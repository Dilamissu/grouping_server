from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.apps import apps

User = apps.get_model('database', 'User')

def register_user(account, name="unknown", password = ""):
    if(account == None):
        raise Exception("Account is None")

    try:
        user = User.objects.get(account=account)
        user = authenticate(account=account,password=password)
        update_last_login(None, user)
        print("User is logged:", user!=None)
        
        return {
            'user': user,
            'tokens': user.tokens()
        }
    except User.DoesNotExist:
        user = User.objects.create_user(account=account, user_name=name,password=password)
        user = authenticate(account=account, password=password)
        update_last_login(None, user)
        print("User is logged:", user!=None)

        return {
            'user': user,
            'tokens': user.tokens()
        }
    except:
        user = User.objects.get(account=account)
        if(user!=None):
            return {
                'error-code': "Wrong_password",
                'error': "Wrong password, please try again"
            }
        else:
            return {
                'error-code': "Unexpected_error",
                'error': "Unexpected error, please contact admin"
            }