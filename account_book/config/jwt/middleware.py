from django.core.exceptions import ObjectDoesNotExist

from users.models import User
from users.tokens import decode_token


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("custom middleware before next middleware/view")
        token = request.COOKIES.get('jwt')
        re_token = request.COOKIES.get('jwt_r')
        if token:
            data = decode_token(token)
            try:
                user = User.objects.get(pk=data['userId'])
                request._force_auth_user = user
            except ObjectDoesNotExist:
                pass
        response = self.get_response(request)
        print("custom middleware after response or previous middleware")
        return response
