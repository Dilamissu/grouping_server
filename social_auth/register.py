from django.contrib.auth import authenticate
from django.apps import apps

User = apps.get_model('database', 'User')

def register_social_user(account, email, name):
    print("register_social_user() called")

    try:
        user = User.objects.get(account=account)
        user = authenticate(account=account)
        print("User is logged: "+user)

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
        user = User.objects.create_user(account=account,email=email, user_name=name)
        user = authenticate(account=account)
        print("User is created: "+user)
   
        print({
            'user': user,
            'tokens': user.tokens().get('access')
        })

        return {
            # 'user': user,
            'tokens': user.tokens()
        }