from django.urls import path
from .views import TaskListView

urlpatterns = [
	# Task Management
	path('', TaskListView.as_view(), name='task_list'),
]

'''
	path('',),
	path('<int:pk>/',),
	path('<int:pk>/',),
	path('<int:pk>/',),
	path('<int:pk>/',),
	# Task Operations
	path('<int:pk>/assign/',),
	path('<int:pk>/comments/',),
	path('<int:pk>/comments/',),
	path('<int:pk>/history/',),

GET /api/tasks/ (with filtering, search, pagination)
POST /api/tasks/
GET /api/tasks/{id}/
PUT /api/tasks/{id}/
PATCH /api/tasks/{id}/
DELETE /api/tasks/{id}/
---
POST /api/tasks/{id}/assign/
POST /api/tasks/{id}/comments/
GET /api/tasks/{id}/comments/
GET /api/tasks/{id}/history/
'''