from rest_framework import serializers
from django.contrib.auth import get_user_model

# get_user_model() to get our AbstractUser
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
	# Security purposes, won't show password as API response
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['id', 'username', 'password', 'email']

	def create(self, validated_data):
		# create_user() encrypts data
		return User.objects.create_user(
			username=validated_data['username'],
			email=validated_data['email'],
			password=validated_data['password'],
		)