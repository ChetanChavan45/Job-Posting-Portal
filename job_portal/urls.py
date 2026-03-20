from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from users.views import RegisterAPI, LoginAPI
from jobs.views import JobViewSet, ApplicationViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Custom postman testing API paths
    path('api/register/', RegisterAPI.as_view(), name='postman_register'),
    path('api/login/', LoginAPI.as_view(), name='postman_login'),
    path('api/jobs/', JobViewSet.as_view({'get': 'list'}), name='postman_jobs_list'),
    path('api/jobs/create/', JobViewSet.as_view({'post': 'create'}), name='postman_jobs_create'),
    path('api/apply/', ApplicationViewSet.as_view({'post': 'create'}), name='postman_apply'),

    # Existing standard router-based API endpoints
    # Existing standard router-based API endpoints
    path('api/', include('jobs.urls')),
    path('api/auth/', include('users.urls')),

    # Frontend pages
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('jobs/', TemplateView.as_view(template_name='jobs/job_list.html'), name='job_list'),
    path('jobs/<int:pk>/', TemplateView.as_view(template_name='jobs/job_detail.html'), name='job_detail'),
    path('dashboard/candidate/', TemplateView.as_view(template_name='dashboard/candidate.html'), name='candidate_dashboard'),
    path('dashboard/employer/', TemplateView.as_view(template_name='dashboard/employer.html'), name='employer_dashboard'),
    path('login/', TemplateView.as_view(template_name='users/login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='users/register.html'), name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
