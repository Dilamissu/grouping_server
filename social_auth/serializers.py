import requests
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.fields import empty
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
            return {
                'error-code': 'invalid_token',
                'error':'The token is invalid or expired. Please login again.'
            }

        if user_data['aud'] != os.environ.get(env_key+'WEB') and user_data['aud'] != os.environ.get(env_key+'IOS') and user_data['aud'] != os.environ.get(env_key+'ANDROID'):
            print(os.environ.get(env_key))
            raise AuthenticationFailed('oops, who are you?')

        return register.register_user(
            account = user_data['sub'],
            name = user_data['name'])


class LineSocialAuthSerializer(serializers.Serializer):
    def placeholder():
        pass

class GitHubSocialAuthSerializer(serializers.Serializer):

    def validate(self, attrs):

        if not os.environ.get('AUTH_CODE'):
            return {
                'error-code': 'no_code',
                'error' : 'No code in temparary storage, please send the oauth request again'
            }
        else:
            # print(os.environ.get('AUTH_CODE'))
            body = {
                'client_id':os.environ.get('GITHUB_CLIENT_ID'),
                'client_secret':os.environ.get('GITHUB_CLIENT_SECRET'),
                'code':os.environ.get('AUTH_CODE'),
                'redirect_uri':'http://localhost:5000/',
            }
            result = requests.post('https://github.com/login/oauth/access_token',json = body,headers={'Accept': 'application/json'})
            result = result.json()
            if 'access_token' in result:
                print(result['access_token'])
                user = requests.get('https://api.github.com/user',
                                    headers={
                                        'Accept': 'application/json',
                                        'Authorization': 'Bearer '+result['access_token']
                                        },
                                    )
                user=user.json()
                print(user)
                return register.register_user(
                    account=user['id'],
                    name=user['login']
                )
            else:
                print(result)
                return {
                    'error-code': 'no_access_code',
                    'error':'code handle process failed'
                }
        

class CallbackSerializer(serializers.Serializer):

    _dict = {}

    def __init__(self, instance=None, data=..., **kwargs):
        self._dict.update(kwargs)
        super().__init__(instance, data)

    def validate(self, attrs):
        # print(attrs)
        if 'code' not in self._dict:
            raise AuthenticationFailed('Auth consent denied')
        else:
            os.environ['AUTH_CODE'] = self._dict.get('code')
            return os.environ.get('AUTH_CODE')

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh_token']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            return {
                'error-code': 'invalid_token',
                'error':'The token is invalid or expired. Please login again.'
            }