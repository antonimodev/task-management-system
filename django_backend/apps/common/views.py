from django.http import (
	JsonResponse,
	HttpRequest,
	HttpResponse,
)
from django.shortcuts import render

def health_check(request: HttpRequest) -> JsonResponse:
	return JsonResponse({"status": "ok"})

def home(request: HttpRequest) -> HttpResponse:
	return render(request, "home.html")