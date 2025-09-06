from typing import (
	Dict,
	Any,
)
from rest_framework import serializers
from django.contrib.auth import get_user_model

# get_user_model() to always reference the current user model,
# ensuring compatibility if iy changes in the future
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
	# Security purposes, won't show password as API response
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['username', 'password', 'nickname', 'email']

	def create(self, validated_data: Dict[str, Any]):
		# create_user() encrypts data
		return User.objects.create_user(
			username=validated_data['username'],
			email=validated_data['email'],
			nickname=validated_data.get('nickname', ''),
			password=validated_data['password'],
		)