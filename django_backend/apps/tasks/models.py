from django.db import models
""" from django.conf import settings

class Task(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	completed = models.BooleanField(default=False)

	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='task'
	) """