from django.urls import path
from .views import UserCreateView, logout_user
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('logout/', logout_user, name='logout'),
    path('signup/', UserCreateView.as_view(), name='signup'),
]
