from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response as DRFResponse
from rest_framework.permissions import (
	IsAuthenticated,
	IsAdminUser,
)
from rest_framework.decorators import (
	api_view,
	permission_classes,
)
from .serializers import UserSerializer

User = get_user_model()

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

	def get_queryset(self) -> QuerySet:
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

	def get_queryset(self) -> QuerySet:
		user = self.request.user
		if user.is_staff:
			return User.objects.all()
		else:
			return User.objects.filter(pk=user.pk)

# GET
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request: Request) -> DRFResponse:
	serializer = UserSerializer(request.user)
	return DRFResponse(serializer.data)