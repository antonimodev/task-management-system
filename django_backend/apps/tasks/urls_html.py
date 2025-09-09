from django.urls import path
from .views import (
	add_task_view,
	view_tasks_view,
)

app_name = "tasks_html"

urlpatterns = [
	path('add/', add_task_view, name='add_task'),
	path('view/', view_tasks_view, name='view_task'),
]