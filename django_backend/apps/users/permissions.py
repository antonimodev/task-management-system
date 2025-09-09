from rest_framework.permissions import (
	BasePermission,
)
from rest_framework.request import Request
from typing import Any

class IsSelfOrReadOnly(BasePermission):
	def has_object_permission(self, request: Request, obj: Any) -> bool:
		if request.method == 'GET':
			if not obj.is_staff and not obj.is_superuser:
				return True
			if obj.pk == request.user.pk:
				return True
		elif request.method == 'PUT':
			return obj.pk == request.user.pk or request.user.is_staff
		return False