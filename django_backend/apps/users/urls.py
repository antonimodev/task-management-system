from django.urls import path

from .views import (
	UserListView,
	UserDetailUpdateView,
	current_user,
)

# User Management
urlpatterns = [
	path('', UserListView.as_view(), name='user_list'),
	path('<int:pk>/', UserDetailUpdateView.as_view(), name='user_detail_update'),
	path('me/', current_user, name='current_user'),
]