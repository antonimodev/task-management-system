from django.urls import path
from rest_framework_simplejwt.views import (
	TokenObtainPairView,
	TokenRefreshView,
	TokenBlacklistView,
)
from .views import (
	RegisterView,
	UserListView,
	UserDetailView,
	UserUpdateView,
	current_user,
)

urlpatterns = [
	# Authentication Endpoints
	path('register/', RegisterView.as_view(), name='register'),
	path('login/', TokenObtainPairView.as_view(), name='login'),
	path('logout/', TokenBlacklistView.as_view(), name='logout'),
	path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	# User Management
	path('users/', UserListView.as_view(), name='user_list'),
	path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
	path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
	path('users/me/', current_user, name='current_user'),
]