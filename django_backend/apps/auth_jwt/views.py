import requests
from django.shortcuts import (
	render,
    redirect,
)
from django.http import HttpRequest, HttpResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny
from apps.users.serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        nickname = request.POST.get("nickname")
        password = request.POST.get("password")
        password2 = request.POST.get("confirm-password")
        if password != password2:
            return render(
                request,
                "register.html",
                {"error": "Passwords don't match"},
            )
        data = {
            "username": username,
            "email": email,
            "password": password,
            "nickname": nickname,
        }
		# 'web' is service name inside docker-compose.yml with django
        api_url = f"http://web:8000/api/auth/register/"
        try:
            response = requests.post(api_url, json=data)
            if response.status_code == 201:
                return redirect("auth_jwt_html:login")
            else:
                error = response.json()
        except Exception as e:
            error = {"error": str(e)}
        return render(request, "register.html", {"error": error, "form_data": data})
    return render(request, "register.html")

def login_view(request: HttpRequest) -> HttpResponse:
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")
		data = {
			"username": username,
			"password": password,
		}
		api_url = f"http://web:8000/api/auth/login/"
		try:
			response = requests.post(api_url, json=data)
			if response.status_code == 200:
				tokens = response.json()
				request.session['access_token'] = tokens['access']
				request.session['refresh_token'] = tokens['refresh']
				return redirect("home")
			else:
				error = "Invalid username or password"
		except Exception as e:
			error = f"Connection error: {str(e)}"
		return render(request, "login.html", {"error": error, "form_data": data})
	return render(request, "login.html")

def logout_view(request: HttpRequest) -> HttpResponse:
	if 'access_token' in request.session:
		del request.session['access_token']
	if 'refresh_token' in request.session:
		del request.session['refresh_token']
	return redirect("home")