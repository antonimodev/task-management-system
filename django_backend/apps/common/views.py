from django.http import (
	JsonResponse,
	HttpRequest,
	HttpResponse,
)
from django.shortcuts import render

def health_check(request: HttpRequest) -> JsonResponse:
	return JsonResponse({"status": "ok"})

def home(request: HttpRequest) -> HttpResponse:
	is_authenticated = 'access_token' in request.session
	return render(request, "home.html", {"is_authenticated": is_authenticated})