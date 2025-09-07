from django.urls import path
from .views import (
	TaskListView,
	TaskDetailView,
	TaskAssignView
)

urlpatterns = [
	# Task Management
	path('', TaskListView.as_view(), name='task_list'),
	path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
	# Pending test with frontend
	path('<int:pk>/assign', TaskAssignView.as_view(), name='task_assignment'),
]

'''
	# Task Operations
	path('<int:pk>/comments/',),
	path('<int:pk>/comments/',),
	path('<int:pk>/history/',),
---
POST /api/tasks/{id}/comments/
GET /api/tasks/{id}/comments/
GET /api/tasks/{id}/history/
'''