from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from . import google, register
# from grouping_project_backend.models import UserManager, User
from dotenv import load_dotenv
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

import os

load_dotenv()

class LoginSerializer(serializers.Serializer):
    account = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    def validate(self, attrs):
        print("LoginSerializer.validate() called")
        self.account = attrs.get('account')
        self.password = attrs.get('password')
        return register.register_user(
            account = self.account,
            password = self.password
        )

# The toutorial's code is at https://github.com/CryceTruly/incomeexpensesapi/tree/master/social_auth
class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        env_key = "GOOGLE_CLIENT_ID_"
        user_data = google.Google.validate_id_token(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != os.environ.get(env_key+'WEB') and user_data['aud'] != os.environ.get(env_key+'IOS') and user_data['aud'] != os.environ.get(env_key+'ANDROID'):
            print(os.environ.get(env_key))
            raise AuthenticationFailed('oops, who are you?')

        return register.register_user(
            account = user_data['sub'],
            name = user_data['name'])


class LineSocialAuthSerializer:
    def placeholder():
        pass

class GitHubSocialAuthSerializer:
    def placeholder():
        pass

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh_token']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError('The token is invalid or expired.')