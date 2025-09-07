from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.common.models import SoftDeleteModel

# Recommended in Django doc, this allows customize user in the future easily
class User(SoftDeleteModel, AbstractUser):
	nickname = models.CharField(max_length=20, blank=False, null=False)

	def __str__ (self) -> str:
		return self.username
