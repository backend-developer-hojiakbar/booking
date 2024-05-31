from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User, PhoneToken
from rest_framework.decorators import action
from .serializers import *
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.custom_jwt import MyTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.utils import generate_token, verify_token
from rest_framework import status, generics
from drf_yasg.utils import swagger_auto_schema
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from drf_yasg import openapi


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post', 'get', 'patch']

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return UserSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    )
    @action(detail=False, methods=['post'], url_path="sms/send")
    def send_token(self, request):
        phone = request.data.get('phone_number')
        token = generate_token(phone)
        if token:
            return Response(
                {"message": "Please verify your phone number", "status": "send"}
            )
        return Response(
            {"status": "error", "message": "Phone number is not verified"},
        )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                'token': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    )
    @action(detail=False, methods=['post'], url_path="sms/verify")
    def verify(self, request):
        phone = request.data.get('phone_number')
        token = request.data.get('token')
        if verify_token(phone, token):
            return Response({
                "message": "Verified"
            }, status=200)
        return Response({"message": "Phone number or token is not valid"}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        user_serializer = self.get_serializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        phone = PhoneToken.objects.get(phone_number=request.data.get('phone_number'))
        if phone.is_verified == True:
            user = user_serializer.save()
            user.is_active = True
            tokens = user.tokens()
            user.save()
            return Response({
                "access_token": str(tokens.get('access')),
                "refresh_token": str(tokens.get('refresh'))
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Please verify your phone number'
            }, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'we have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordResetConfirm(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message': 'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': 'credentials is valid', 'uidb64': uidb64, 'token': token},
                            status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            return Response({'message': 'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': "password reset is succesful"}, status=status.HTTP_200_OK)


class LogoutApiView(GenericAPIView):
    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)