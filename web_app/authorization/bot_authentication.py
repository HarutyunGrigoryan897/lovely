from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


class BotAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        expected = f"Bearer {settings.API_SECRET}"
        if auth_header != expected:
            raise AuthenticationFailed("Invalid or missing Bearer token")

        return (None, None)