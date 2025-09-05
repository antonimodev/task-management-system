from django.db import models
from django.contrib.auth.models import AbstractUser

# Recommended in Django doc, this allows customize user in the future easily
class User(AbstractUser):
	pass
