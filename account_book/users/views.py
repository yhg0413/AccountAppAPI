from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.views import APIView


from .models import User
from .permissions_util import IsLoginOrLogout
from .serializers import UserSerializer
from .tokens import *
from django.contrib.auth.hashers import check_password
# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(data=serializer.data)


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [IsLoginOrLogout]

    @action(methods=['POST'], detail=False)
    def login(self,request):
        email = request.data['email']
        password = request.data['password']
        try:
            user = User.objects.get(
                email=email
            )
            if not user.check_password(password):
                raise ObjectDoesNotExist
            
            payload = {
                "iss": "account_book_admin",
                "userId": user.id,
                "email": email,
            }
            access_token = generate_token(payload, "access")
            refresh_token = generate_token(payload, "refresh")
            data = {
                "results": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
            }
            r_status = status.HTTP_200_OK
            response = Response(data=data, status=r_status)
            response.set_cookie(key='jwt', value=access_token, httponly=True)
            response.set_cookie(key='jwt_r', value=refresh_token, httponly=True)
            return response
        except ObjectDoesNotExist:
            data = {
                "results": {
                    "msg": "아이디 또는 비밀번호가 옳바르지 않습니다.",
                    "code": "E4010"
                }
            }
            r_status = status.HTTP_401_UNAUTHORIZED
        except Exception as e:
            print(str(e))
            data = {
                "results": {
                    "msg": "정상적인 접근이 아닙니다.",
                    "code": "E5000"
                }
            }
            r_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(data=data, status=r_status)

    @action(methods=['GET'], detail=False)
    def logout(self,request):
        data = {
            "result": {
                "msg": "로그아웃 되었습니다"
            }
        }
        r_status = status.HTTP_200_OK
        response = Response(data, r_status)
        response.delete_cookie('jwt')
        response.delete_cookie('jwt_r')

        return response



