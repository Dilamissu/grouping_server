from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import (
    LoginSerializer, GoogleSocialAuthSerializer, LineSocialAuthSerializer, GitHubSocialAuthSerializer, LogoutSerializer)
"""
conda activate django_4_2_2
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

"""

# Create your views here.
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        print("LoginView.post() called")
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if 'error' in serializer.validated_data:
            return Response((serializer.validated_data)['error'], status=status.HTTP_401_UNAUTHORIZED)
        
        data = (serializer.validated_data)['tokens']['access']
        print(data)
        return Response(data, status=status.HTTP_200_OK)

class GoogleSocialAuthView(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        print("GoogleSocialAuthView.post() called")
        print(request.data)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)['tokens']['access']
        # print(data['tokens']['access'])
        return Response(data, status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_200_OK)

class LineSocialAuthView(GenericAPIView):
    serializer_class = LineSocialAuthSerializer

    def post(self, request):
        print("GoogleSocialAuthView.post() called")


class GitHubSocialAuthView(GenericAPIView):
    serializer_class = GitHubSocialAuthSerializer

    def get(self, request):
        pass

class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)