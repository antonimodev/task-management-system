from django.urls import path
from .views import (
	register_page,
	login_page,
)

app_name = 'auth_jwt_html'

urlpatterns = [
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    #path('logout/', TokenBlacklistView.as_view(), name='logout'),
    #path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]