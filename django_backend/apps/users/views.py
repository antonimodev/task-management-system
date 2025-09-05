from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import (
	api_view,
	permission_classes,
)
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
)
from django.contrib.auth import get_user_model
from .serializers import UserSerializer


User = get_user_model()

class RegisterView(generics.CreateAPIView):
	serializer_class = UserSerializer
	permission_classes = [AllowAny]

# USER MANAGEMENT

# GET
class UserListView(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [IsAdminUser]

# GET
class UserDetailView(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_staff:
			return User.objects.all()
		else:
			return User.objects.filter(pk=user.pk)

# PUT
class UserUpdateView(generics.UpdateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_staff:
			return User.objects.all()
		else:
			return User.objects.filter(pk=user.pk)

# GET
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
	serializer = UserSerializer(request.user)
	return Response(serializer.data)