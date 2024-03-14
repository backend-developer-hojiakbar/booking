from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
@api_view(["POST",])
def logout_user(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response({"Message": "Siz saytdan chiqdingiz qayta kirish uchun login qiling"}, status=status.HTTP_200_OK)
