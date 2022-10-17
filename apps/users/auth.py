# _*_ encoding:utf-8 _*_

from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token


class TokenAuth(BaseAuthentication):
    def authenticate(self, request):
        request_token = get_authorization_header(request)
        if not request_token:
            raise AuthenticationFailed("缺少token")
        token_obj = Token.objects.filter(key=request_token)
        if not token_obj:
            raise AuthenticationFailed("无效的token")
        return token_obj[0].user.username, None
