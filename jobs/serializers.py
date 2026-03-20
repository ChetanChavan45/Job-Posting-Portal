from rest_framework import serializers
from .models import Job, Application

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at')


class ApplicationSerializer(serializers.ModelSerializer):
    job_details = JobSerializer(source='job', read_only=True)
    applicant_name = serializers.CharField(source='user.username', read_only=True)
    applicant_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('user', 'applied_at', 'status')

class EmployerApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('status',)
