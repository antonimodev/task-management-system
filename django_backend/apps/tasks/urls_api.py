from django.urls import path
from .views import (
	TaskListView,
	TaskDetailView,
	TaskAssignView
)

app_name = "tasks_api"

urlpatterns = [
	path('', TaskListView.as_view(), name='task_list'),
	path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
	path('<int:pk>/assign', TaskAssignView.as_view(), name='task_assignment'),
]
