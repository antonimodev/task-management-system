import requests
from django_filters.rest_framework import DjangoFilterBackend
from django.http import (
	HttpRequest,
	HttpResponse,
)
from django.conf import settings
from django.shortcuts import (
	render,
	redirect,
	get_object_or_404,
)
from apps.users.models import User
from apps.tasks.models import (
	Tag,
	Task,
	TaskAssignment,
)
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

	def perform_create(self, serializer):
		serializer.save(created_by=self.request.user)

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


# This 2 functions are made to check token validation, if not valid redirect to login
def clear_tokens(request):
	request.session.pop('access_token', None)
	request.session.pop('refresh_token', None)

def check_token_or_redirect(request: HttpRequest, test_url: str, redirect_url: str = 'auth_jwt_html:login'):
	if 'access_token' not in request.session:
		clear_tokens(request)
		return redirect(redirect_url)
	headers = {'Authorization': f'Bearer {request.session["access_token"]}'}
	try:
		response = requests.get(test_url, headers=headers)
		if response.status_code == 401:
			clear_tokens(request)
			return redirect(redirect_url)
	except Exception:
		clear_tokens(request)
		return redirect(redirect_url)
	return None

# Refactorizing form data to edit and add tasks
def get_task_form_data(request):
    return {
        "title": request.POST.get("title"),
        "description": request.POST.get("description"),
        "status": request.POST.get("status"),
        "priority": request.POST.get("priority"),
        "due_date": request.POST.get("due_date"),
        "estimated_hours": request.POST.get("estimated_hours"),
        "tags": [int(tag) for tag in request.POST.getlist("tags") if tag],
    }


# TASK ACTIONS
def add_task_view(request: HttpRequest) -> HttpResponse:
	test_url = f"{settings.API_BASE_URL}/api/tasks"
	token_check = check_token_or_redirect(request, test_url)
	if token_check:
		return token_check
	if request.method == "POST":
		data = get_task_form_data(request)
		api_url = f"{settings.API_BASE_URL}/api/tasks/"
		headers = {'Authorization': f'Bearer {request.session["access_token"]}'}
		try:
			response = requests.post(api_url, json=data, headers=headers)
			if response.status_code == 201:
				return redirect("tasks_html:view_task")
			else:
				error = response.json()
		except Exception as e:
			error = {"error": str(e)}
		tags = Tag.objects.all()
		return render(request, "add_task.html", {
			"error": error,
			"form_data": data,
			"tags": tags
		})
	else:
		tags = Tag.objects.all()
		return render(request, "add_task.html", {"tags": tags})


def view_tasks_view(request: HttpRequest) -> HttpResponse:
	test_url = f"{settings.API_BASE_URL}/api/tasks"
	token_check = check_token_or_redirect(request, test_url)
	if token_check:
		return token_check

	api_url = f"{settings.API_BASE_URL}/api/tasks/"
	users_url = f"{settings.API_BASE_URL}/api/users/"
	headers = {'Authorization': f'Bearer {request.session["access_token"]}'}
	tasks = []
	users = []
	error = None
	try:
		response = requests.get(api_url, headers=headers)
		if response.status_code == 200:
			tasks = response.json().get('results', [])
		elif response.status_code == 401:
			token_check = check_token_or_redirect(request, test_url)
			if token_check:
				return token_check
		else:
			error = "Error loading tasks"
	except Exception as e:
		error = f"Connection error: {str(e)}"
	try:
		response = requests.get(users_url, headers=headers)
		if response.status_code == 200:
			users = response.json().get('results', [])
	except Exception:
		pass
	return render(request, "view_task.html", {
		"tasks": tasks,
		"users": users,
		"error": error,
	})