from django.core.exceptions import ObjectDoesNotExist

from users.models import User
from users.tokens import decode_token


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token = request.COOKIES.get('jwt')
        refresh_token = request.COOKIES.get('jwt_r')
        new_access_token = None

        if access_token and refresh_token:
            decoded_data, new_access_token = decode_token(access_token,refresh_token)
            if decoded_data:
                try:
                    user = User.objects.get(pk=decoded_data['userId'])
                    request._force_auth_user = user
                except ObjectDoesNotExist:
                    pass

        response = self.get_response(request)
        if new_access_token:
            response.set_cookie(key='jwt',value=new_access_token,httponly=True)

        return response
