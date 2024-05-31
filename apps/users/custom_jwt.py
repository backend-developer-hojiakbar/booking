from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.validators import ValidationError
from apps.users.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")

        user = User.objects.get(phone_number=phone_number)
        attrs["phone_number"] = user.phone_number
        if user:
            if user.check_password(password):
                data = super().validate(attrs)
                refresh = self.get_token(user)
                data["access"] = str(refresh.access_token)
                data["refresh"] = str(refresh)
                return data
            else:
                raise ValidationError({"detail": "username or password is incorrect"})
        else:
            raise ValidationError({"detail": "username or password is incorrect"})

    def get_token(self, user):
        token = super().get_token(user)
        token["phone_number"] = user.phone_number
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    