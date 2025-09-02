from rest_framework import generics, status
from rest_framework.response import Response

from authorization.models import CustomUser
from authorization.serializers import CustomUserSerializer, CustomUserInfoSerializer

class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomUserRetrieveView(generics.GenericAPIView):
    serializer_class = CustomUserInfoSerializer
    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        telegram_id = request.query_params.get("telegram_id")
        if not telegram_id:
            return Response({"detail": "telegram_id query parameter is required."}, status=400)

        try:
            user = CustomUser.objects.get(telegram_id=telegram_id)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)
        except Exception:
            return Response({"detail": "Something went wrong."}, status=500)