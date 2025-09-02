from rest_framework import generics, status
from rest_framework.views import APIView
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
        
class CheckAdminView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        telegram_id = request.query_params.get("telegram_id")
        if not telegram_id:
            return Response({"detail": "telegram_id query parameter is required."}, status=400)

        try:
            user = CustomUser.objects.get(telegram_id=telegram_id)
            return Response({"is_admin": user.is_superuser}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)
        except Exception:
            return Response({"detail": "Something went wrong."}, status=500)

class AdminListView(APIView):

    def get(self, request):
        admins = CustomUser.objects.filter(is_superuser=True).values("telegram_id", "username", "first_name", "last_name")
        return Response(list(admins))
    
class ApproveUserView(APIView):
    def post(self, request, telegram_id):
        try:
            user = CustomUser.objects.get(telegram_id=telegram_id)
            user.approved = True
            user.save()
            return Response({"detail": "User approved successfully."})
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class RejectUserView(APIView):
    def post(self, request, telegram_id):
        try:
            user = CustomUser.objects.get(telegram_id=telegram_id)
            user.approved = False
            user.save()
            return Response({"detail": "User rejected successfully."})
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)