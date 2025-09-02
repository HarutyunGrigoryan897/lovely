from rest_framework import serializers
from authorization.models import CustomUser

from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(required=True)
    username = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ["telegram_id", "username", "first_name", "last_name", "approved"]
        validators = []

    def create(self, validated_data):
        telegram_id = validated_data.get("telegram_id")
        user, created = CustomUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                "username": validated_data.get("username") or "",
                "first_name": validated_data.get("first_name") or "",
                "last_name": validated_data.get("last_name") or "",
                "approved": False,
            }
        )

        if not created:
            # Update fields if provided
            if validated_data.get("username") is not None:
                user.username = validated_data.get("username")
            if validated_data.get("first_name") is not None:
                user.first_name = validated_data.get("first_name")
            if validated_data.get("last_name") is not None:
                user.last_name = validated_data.get("last_name")
            user.save()

        return user


class CustomUserInfoSerializer(serializers.ModelSerializer):
    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["telegram_id", "username", "first_name", "last_name", "approved", "date_joined"]

    def get_date_joined(self, obj):
        return obj.date_joined.strftime("%d %B %Y")