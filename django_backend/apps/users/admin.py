from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# Register the custom User, so all users can be managed from the admin panel
admin.site.register(User, UserAdmin)
