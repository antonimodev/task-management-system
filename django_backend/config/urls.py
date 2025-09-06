from django.contrib import admin
from django.urls import (
	path,
	include,
)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
	# COMMON
	path('', include('apps.common.urls')),
	# AUTH
	path('api/auth/', include('apps.auth_jwt.urls')),
	# USERS
	path('api/users/', include('apps.users.urls')),
	# TASK MANAGEMENT
	path('api/tasks/', include('apps.tasks.urls')),
]
