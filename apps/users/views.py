from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi

from .models import UserProfile


# Create your views here.


class UserLogin(APIView):
    authentication_classes = []

    @swagger_auto_schema(
        tags=["用户管理"],
        operation_description="用户登录",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password"],
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING, description="用户名"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, description="登录密码")
            }
        ),
        responses={200: openapi.Response(
            description="OK",
            examples={
                "application/json": {
                    "status": "success",
                    "token": "5388ed9b6394beb2864d0c117295bd345ff033a2"
                }
            },
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "status": openapi.Schema(type=openapi.TYPE_STRING, description="接口状态"),
                    "token": openapi.Schema(type=openapi.TYPE_STRING, description="用户令牌")
                }
            )
        )}
    )
    def post(self, request):
        username = request.data["username"]
        password = request.data[u"password"]
        userprofile = UserProfile.objects.filter(username=username)
        user = None
        if len(userprofile) > 0:
            userprofile = userprofile[0]
            user = authenticate(username=userprofile.username, password=password)
        token_key = ""
        if user is not None:
            if user.is_active:
                token = Token.objects.filter(user=user)
                if len(token) == 0:
                    token = Token.objects.create(user=user)
                    token_key = token.key
                else:
                    token_key = token[0].generate_key()
                    token.update(key=token_key)
        else:
            return Response({"status": "error", "msg": "用户名或密码错误"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"status": "success", "token": token_key}, status=status.HTTP_200_OK)
