from google.oauth2 import id_token
from google.auth.transport import requests

class Google:
    @staticmethod
    def validate_id_token(auth_token):
        try:
            idinfo = id_token.verify_oauth2_token(auth_token, requests.Request())

            if 'accounts.google.com' in idinfo['iss']:
                return idinfo
            
        except:
            return "Something went wrong with the Google authentication."
        