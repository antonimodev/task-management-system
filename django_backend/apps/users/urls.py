from django.urls import path

from .views import (
	UserListView,
	UserDetailView,
	UserUpdateView,
	current_user,
)

# User Management
urlpatterns = [
	path('', UserListView.as_view(), name='user_list'),
	path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
	path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
	path('me/', current_user, name='current_user'),
]