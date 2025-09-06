from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response as DRFResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
	IsAuthenticated,
	IsAdminUser,
)
from rest_framework.decorators import (
	api_view,
	permission_classes,
)
from .serializers import UserSerializer
from .permissions import IsSelfOrReadOnly

User = get_user_model()

# USER MANAGEMENT

class UserListPagination(PageNumberPagination):
	page_size = 10
	page_size_query_param = 'page_size'
	max_page_size = 20 # To protect max page size of API

# GET
class UserListView(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	pagination_class = UserListPagination
	permission_classes = [IsAdminUser]

# GET & PUT
class UserDetailUpdateView(generics.RetrieveUpdateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [IsAuthenticated, IsSelfOrReadOnly]

# GET
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request: Request) -> DRFResponse:
	serializer = UserSerializer(request.user)
	return DRFResponse(serializer.data)