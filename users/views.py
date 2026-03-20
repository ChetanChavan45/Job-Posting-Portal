from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from django.contrib.auth import login, logout

class RegisterAPI(generics.GenericAPIView):
    """
    API endpoint for registering a new user (Job Seeker or Employer).
    Returns basic user details and a token upon successful registration.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        login(request, user) # logging the user in session too for mixed auth
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })

class LoginAPI(generics.GenericAPIView):
    """
    API endpoint to log in as a user and retrieve an auth token.
    """
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, _ = Token.objects.get_or_create(user=user)
        login(request, user) # Cookie session login
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })

class LogoutAPI(APIView):
    """
    API endpoint to securely log out the current user and destroy their token.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({"message": "Successfully logged out."})

class UserAPI(generics.RetrieveAPIView):
    """
    API endpoint to fetch the currently authenticated user's details.
    """
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
