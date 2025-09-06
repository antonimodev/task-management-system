from rest_framework import (
	generics,
	filters
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializer import TaskSerializer

class TaskListPagination(PageNumberPagination):
	page_size = 10
	page_size_query_param = 'page_size'
	max_page_size = 30 # To protect max page size of API

# GET POST
class TaskListView(generics.ListCreateAPIView):
	queryset = Task.objects.all()
	serializer_class = TaskSerializer
	permission_classes = [IsAuthenticated]
	# Pagination
	pagination_class = TaskListPagination
	# Searching
	filter_backends = [DjangoFilterBackend, filters.SearchFilter]
	search_fields = ['title', 'priority']
	# Filtering
	filterset_fields = ['status', 'priority', 'assigned_to', 'created_by', 'tags']

# GET PUT PATCH DELETE
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Task.objects.all()
	serializer_class = TaskSerializer
	permission_classes = [IsAuthenticated]