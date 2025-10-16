from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from authorization.models import CustomUser
from authorization.serializers import CustomUserSerializer, CustomUserInfoSerializer
from authorization.bot_authentication import BotAuthentication


class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [BotAuthentication]


class CustomUserRetrieveView(generics.GenericAPIView):
    serializer_class = CustomUserInfoSerializer
    queryset = CustomUser.objects.all()
    authentication_classes = [BotAuthentication]

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
    authentication_classes = [BotAuthentication]

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
    authentication_classes = [BotAuthentication]

    def get(self, request):
        admins = CustomUser.objects.filter(is_superuser=True).values("telegram_id", "username", "first_name", "last_name")
        return Response(list(admins))

    
class ApproveUserView(APIView):
    authentication_classes = [BotAuthentication]
    
    def post(self, request, telegram_id):
        try:
            user = CustomUser.objects.get(telegram_id=telegram_id)
            user.approved = True
            
            # Set default user level if provided
            user_level = request.data.get('user_level', 'user')
            if user_level in dict(CustomUser.USER_LEVEL_CHOICES).keys():
                user.user_level = user_level
            
            user.save()
            return Response({
                "detail": "User approved successfully.",
                "user_level": user.user_level
            })
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class SetUserLevelView(APIView):
    """Set user level (User/Dealer/VIP/Partner)"""
    authentication_classes = [BotAuthentication]
    
    def post(self, request, telegram_id):
        try:
            user = CustomUser.objects.get(telegram_id=telegram_id)
            user_level = request.data.get('user_level')
            
            if not user_level:
                return Response(
                    {"detail": "user_level is required."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if user_level not in dict(CustomUser.USER_LEVEL_CHOICES).keys():
                return Response(
                    {"detail": f"Invalid user_level. Must be one of: {', '.join(dict(CustomUser.USER_LEVEL_CHOICES).keys())}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.user_level = user_level
            user.save()
            
            return Response({
                "detail": "User level updated successfully.",
                "user_level": user.user_level,
                "price_multiplier": user.get_price_multiplier()
            })
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class RejectUserView(APIView):
    authentication_classes = [BotAuthentication]
    
    def post(self, request, telegram_id):
        try:
            user = CustomUser.objects.get(telegram_id=telegram_id)
            user.approved = False
            user.save()
            return Response({"detail": "User rejected successfully."})
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)