from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer, EmployerApplicationUpdateSerializer
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

class IsEmployerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'employer'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user


class JobViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing job postings.
    Employers can create, update, and delete jobs.
    Job Seekers (and unauthenticated users) can only view jobs.
    """
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer
    permission_classes = [IsEmployerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['location', 'job_type', 'salary']
    search_fields = ['title', 'company', 'skills', 'description']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def my_jobs(self, request):
        if request.user.role == 'employer':
            jobs = Job.objects.filter(created_by=request.user).order_by('-created_at')
            page = self.paginate_queryset(jobs)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(jobs, many=True)
            return Response(serializer.data)
        return Response({"detail": "Not an employer."}, status=403)


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing job applications.
    Job Seekers can apply for jobs and view their applications.
    Employers can view applications for their posted jobs and update statuses.
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'employer':
            return Application.objects.filter(job__created_by=user).order_by('-applied_at')
        return Application.objects.filter(user=user).order_by('-applied_at')

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH'] and self.request.user.role == 'employer':
            return EmployerApplicationUpdateSerializer
        return ApplicationSerializer

    def perform_create(self, serializer):
        job_id = self.request.data.get('job')
        if not job_id:
            raise serializers.ValidationError({"job": "Job ID is required."})
        job = get_object_or_404(Job, id=job_id)
        
        resume = self.request.data.get('resume')
        if resume and not resume.name.lower().endswith('.pdf'):
            raise serializers.ValidationError({"resume": "Only PDF files are allowed."})

        # Ensure job seeker doesn't apply twice
        if Application.objects.filter(user=self.request.user, job=job).exists():
            raise serializers.ValidationError({"detail": "You have already applied for this job."})

        serializer.save(user=self.request.user, job=job)

    def update(self, request, *args, **kwargs):
        # Only employer can update status
        application = self.get_object()
        if request.user.role != 'employer' or application.job.created_by != request.user:
            return Response({"detail": "Permission denied."}, status=403)
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['GET'])
    def stats(self, request):
        if request.user.role == 'employer':
            jobs = Job.objects.filter(created_by=request.user)
            total_jobs = jobs.count()
            total_applications = Application.objects.filter(job__in=jobs).count()
            selected_candidates = Application.objects.filter(job__in=jobs, status='selected').count()
            return Response({
                "total_jobs": total_jobs,
                "total_applications": total_applications,
                "selected_candidates": selected_candidates
            })
        return Response({"detail": "Not an employer."}, status=403)
