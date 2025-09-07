from django.db import models
from django.db.models import UniqueConstraint
from apps.users.models import User
from apps.common.models import SoftDeleteModel

STATUS_CHOICES = [
	('pending', 'Pending'),
	('in_progress', 'In Progress'),
	('completed', 'Completed'),
]

PRIORITY_CHOICES = [
	('low', 'Low'),
	('medium', 'Medium'),
	('high', 'High'),
	('extreme', 'Extreme'),
]

class Tag(models.Model):
	name = models.CharField(max_length=50, unique=True)

	def __str__(self):
			return self.name

class Task(SoftDeleteModel, models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	status = models.CharField(choices=STATUS_CHOICES, max_length=20)
	priority = models.CharField(choices=PRIORITY_CHOICES, max_length=20)
	due_date = models.DateTimeField()
	estimated_hours = models.DecimalField(max_digits=5, decimal_places=2)
	actual_hours = models.DecimalField(null=True, max_digits=5, decimal_places=2)

	# Relationships
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
	assigned_to = models.ManyToManyField(User, through='TaskAssignment', through_fields=('task', 'user'), related_name='assigned_tasks')
	tags = models.ManyToManyField(Tag, related_name='tasks')
	parent_task = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='subtasks')

	# Metadata
	metadata = models.JSONField(default=dict, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	is_archived = models.BooleanField(default=False)

'''
Notes:
- Defining a __str__ method for Task would improve admin readability.
I am not adding it to strictly follow the provided technical test requirements.

- Some fields needs more arguments to work properly with Django, so I added
some of them to make it work
'''

class TaskAssignment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	assigned_at = models.DateTimeField(auto_now_add=True)
	assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments_made')

	# Avoid duplicated combinations of users/tasks
	class Meta:
		constraints = [
			UniqueConstraint(fields=['user', 'task'], name="unique_combination"),
		]

	def __str__(self):
		return f"{self.user.username} assigned to {self.task.title} by {self.assigned_by.username}"
