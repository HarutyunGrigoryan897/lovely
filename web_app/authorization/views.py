from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from authorization.models import CustomUser
from shop.models import Order
from authorization.serializers import (CustomUserSerializer, CustomUserInfoSerializer, 
                                       OrderSerializer, ShippingSerializer)
from authorization.bot_authentication import BotAuthentication

from django.shortcuts import get_object_or_404


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
            user.save()
            return Response({"detail": "User approved successfully."})
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


class SetUserLevelView(APIView):
    authentication_classes = [BotAuthentication]
    
    def post(self, request, telegram_id):
        """Set user level after approval"""
        from authorization.models import UserLevel
        
        try:
            user = CustomUser.objects.get(telegram_id=telegram_id)
            level_name = request.data.get('level_name')
            
            if not level_name:
                return Response({"detail": "level_name is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Get the user level
            try:
                user_level = UserLevel.objects.get(name=level_name, is_active=True)
            except UserLevel.DoesNotExist:
                return Response({"detail": f"User level '{level_name}' not found."}, status=status.HTTP_404_NOT_FOUND)
            
            # Set the user level
            user.user_level = user_level
            user.save()
            
            return Response({
                "detail": "User level set successfully.",
                "level": user_level.get_name_display(),
                "multiplier": str(user_level.multiplier)
            })
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
class WaitingApprovedUsersListView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(approved=False)
    serializer_class = CustomUserSerializer
    authentication_classes = [BotAuthentication]

class WaitingStatusUsersListView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(user_level=None).exclude(is_superuser = True)
    serializer_class = CustomUserSerializer
    authentication_classes = [BotAuthentication]


#Orders

class OrderConfirmedView(APIView):
    authentication_classes = [BotAuthentication]

    def get(self, request, order_id, *args, **kwargs):
        product = get_object_or_404(Order, id=order_id)
        product.status = "confirmed"
        product.save()

        return Response({
            "order": {
                "user_telegram_id": product.user.telegram_id,
                "order_number": product.order_number,
                "status": product.status,
                "total_price": product.total_amount,
            }
        }, status=status.HTTP_200_OK)

class OrderRejectedView(APIView):
    authentication_classes = [BotAuthentication]

    def get(self, request, order_id, *args, **kwargs):
        product = get_object_or_404(Order, id=order_id)
        product.status = "cancelled"
        product.save()

        return Response({
            "order": {
                "user_telegram_id": product.user.telegram_id,
                "order_number": product.order_number,
                "status": product.status,
            }
        }, status=status.HTTP_200_OK)
    
class OrderDeliveredView(APIView):
    authentication_classes = [BotAuthentication]

    def get(self, request, order_id, *args, **kwargs):
        product = get_object_or_404(Order, id=order_id)
        product.status = "delivered"
        product.save()

        return Response({
            "order": {
                "user_telegram_id": product.user.telegram_id,
                "order_number": product.order_number,
                "status": product.status,
                "total_price": product.total_amount,
            }
        }, status=status.HTTP_200_OK)
    
class WaitingConfirmOrdersListView(generics.ListAPIView):
    queryset = Order.objects.filter(status="pending").prefetch_related("items__product__brand")
    serializer_class = OrderSerializer
    authentication_classes = [BotAuthentication]

class WaitingShippingOrdersListView(generics.ListAPIView):
    queryset = Order.objects.filter(status="confirmed").prefetch_related("items__product__brand")
    serializer_class = ShippingSerializer
    authentication_classes = [BotAuthentication]

class OrderHistoryView(generics.ListAPIView):
    queryset = Order.objects.filter(status="delivered").prefetch_related("items__product__brand")
    serializer_class = OrderSerializer
    authentication_classes = [BotAuthentication]