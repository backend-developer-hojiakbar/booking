from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.views import *


router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
# router.register('send-sms', SendSmsCode, basename='send-sms')

urlpatterns = [
    path('', include(router.urls)),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='reset-password-confirm'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
    path('logout/', LogoutApiView.as_view(), name='logout')
] 
