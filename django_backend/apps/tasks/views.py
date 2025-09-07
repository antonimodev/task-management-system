from rest_framework import (
	generics,
	filters,
    status,
)
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from apps.users.models import User
from .models import Task, TaskAssignment
from .serializer import TaskSerializer

class TaskListPagination(PageNumberPagination):
	page_size = 10
	page_size_query_param = 'page_size'
	max_page_size = 30 # To protect max page size of API

# GET POST
class TaskListView(generics.ListCreateAPIView):
	queryset = Task.objects.select_related('created_by', 'parent_task').prefetch_related('assigned_to', 'tags')
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
	queryset = Task.objects.select_related('created_by', 'parent_task').prefetch_related('assigned_to', 'tags')
	serializer_class = TaskSerializer
	permission_classes = [IsAuthenticated]


class TaskAssignView(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request: Request, pk: int) -> Response:
		task = get_object_or_404(Task, pk=pk)

		if not (request.user == task.created_by or request.user.is_staff):
			return Response(
				{'detail': 'Forbidden'},
				status=status.HTTP_403_FORBIDDEN)

		assigned_user_id = request.data.get('assigned_user_id') # Name to get it from frontend
		if not assigned_user_id:
			return Response(
				{'assigned_user_id': 'This field is required.'},
				status=status.HTTP_400_BAD_REQUEST)

		user_assigned = get_object_or_404(User, pk=assigned_user_id)

		if TaskAssignment.objects.filter(task=task, user=user_assigned).exists():
			return Response(
				{'detail': 'User already assigned to this task.'},
				status=status.HTTP_200_OK)

		assignment = TaskAssignment.objects.create(
			task=task,
			user=user_assigned,
			assigned_by=request.user
		)

		return Response(
			{'id': assignment.id, 'assigned': True},
			status=status.HTTP_201_CREATED)