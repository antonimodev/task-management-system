from rest_framework import generics
from rest_framework.permissions import AllowAny
from apps.users.serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]