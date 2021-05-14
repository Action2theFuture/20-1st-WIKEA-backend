import jwt

from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from user.models    import User
from wikea.settings import SECRET_KEY

def authorize(func):
    
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')
            user         = User.objects.get(id=payload['id'])
            request.user = user
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN' }, status=400)

        except Account.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper()