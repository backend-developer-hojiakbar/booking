from rest_framework import serializers
from apps.users.models import User, PhoneToken
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.exceptions import AuthenticationFailed
from django.urls import reverse
from .utils import send_normal_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'email', 'rating', 'rapidlyReply', 'description', 'image', 'role')
        read_only_fields = ('phone_number', )


class CreateUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            rating=validated_data.get('rating'),
            rapidlyReply=validated_data.get('rapidlyReply'),
            description=validated_data.get('description'),
            image=validated_data.get('image'),
            role=validated_data.get('role'),
            phone_number=validated_data.get('phone_number'),
            password=validated_data.get('password'))
        user.is_active = False
        phonetoken = PhoneToken.objects.get(phone_number=user.phone_number)
        if phonetoken.is_verified == True:
            user.save()
            user.set_password("DefaultPassword123#33$33$33")
            user.save()
            return user

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'email', 'rating', 'rapidlyReply', 'description', 'image', 'role')


class PhoneTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneToken
        fields = ['phone_number']


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            current_site = get_current_site(request).domain
            relative_link = reverse('reset-password-confirm', kwargs={'uidb64': uidb64, 'token': token})
            abslink = f"http://{current_site}{relative_link}"
            print(abslink)
            email_body = f"Hi {user.first_name} use the link below to reset your password {abslink}"
            data = {
                'email_body': email_body,
                'email_subject': "Reset your Password",
                'to_email': user.email
            }
            send_normal_email(data)
        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=3, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("reset link is invalid or has expired", 401)
            if password != confirm_password:
                raise AuthenticationFailed("passwords do not match")
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            return AuthenticationFailed("link is invalid or has expired")


class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')