from django.contrib.auth import authenticate
from django.apps import apps

User = apps.get_model('database', 'User')

def register_user(account, name, password = ""):
    print("register_social_user() called")

    try:
        user = User.objects.get(account=account)
        user = authenticate(account=account)
        print("User is logged:", user!=None)

        print({
            'user': user,
            'tokens': user.tokens().get('access')
        })
        
        return {
            # 'user': user,
            'tokens': user.tokens()
        }
    except User.DoesNotExist:
        print("User doesNotExist")
        user = User.objects.create_user(account=account, user_name=name,password=password)
        user = authenticate(account=account, password=password)
        print("User is logged:", user!=None)
   
        print({
            'user': user,
            'tokens': user.tokens().get('access')
        })

        return {
            # 'user': user,
            'tokens': user.tokens()
        }