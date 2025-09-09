from celery import shared_task
from django.utils import timezone
from datetime import timedelta

@shared_task
def check_overdue_tasks():
	from apps.tasks.models import Task
	now = timezone.now()
	updated = Task.objects.filter(due_date__lt=now).exclude(status='completed').update(status='overdue')
	return {"updated": updated}

@shared_task
def cleanup_archived_tasks(days=30):
	from apps.tasks.models import Task
	cutoff = timezone.now() - timedelta(days=days)
	deleted, _ = Task.objects.filter(is_archived=True, updated_at__lt=cutoff).delete()
	return {"deleted": deleted}