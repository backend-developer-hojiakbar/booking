from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=12)

    def validate_phone_number(self, value):
        # Ensure that the phone number is exactly 12 digits long
        if len(value) != 12:
            raise serializers.ValidationError("Telefon raqamingiz 12 raqamdan iborat bo'lishi kerak.")
        return value
