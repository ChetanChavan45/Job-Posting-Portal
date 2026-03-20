from django.urls import path
from .views import RegisterAPI, LoginAPI, LogoutAPI, UserAPI

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register_api'),
    path('login/', LoginAPI.as_view(), name='login_api'),
    path('logout/', LogoutAPI.as_view(), name='logout_api'),
    path('user/', UserAPI.as_view(), name='user_api'),
]
