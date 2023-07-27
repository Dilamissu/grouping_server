from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import (
    GoogleSocialAuthSerializer, LineSocialAuthSerializer, GitHubSocialAuthSerializer, LogoutSerializer)

# Create your views here.
class GoogleSocialAuthView(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        print("GoogleSocialAuthView.post() called")
        print(request.data)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
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