from rest_framework import serializers
from main.models import *

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'id',
			'username',
			'password',
			'email',
			'first_name',
			'last_name',
			'timestamp',
			)
		extra_kwargs = {'password':{'write_only': True}}

	def create(self, validated_data):

		user = User(
			username=validated_data['username'],
			email=validated_data['email'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name']
			)
		user.set_password(validated_data['password'])
		user.save()
		return user

class JobSerializer(serializers.ModelSerializer):
	class Meta:
		model = Job
		fields = (
			'id',
			'name',
			'description', 
			'created_at',
			'user_id', 
			)

class InventorySerializer(serializers.ModelSerializer):

	path = serializers.FileField(allow_empty_file=False, use_url=False)

	class Meta:
		model = Inventory 
		fields = (
			'id',
			'description', 
			'path', 
			'uploaded_at', 
			'user_id',
			)

class PlaybookSerializer(serializers.ModelSerializer):

	path = serializers.FileField(allow_empty_file=False, use_url=False)

	class Meta:
		model = Playbook 
		fields = (
			'id', 
			'description', 
			'path', 
			'uploaded_at', 
			'user_id',
			)

class HistorySerializer(serializers.ModelSerializer):
	class Meta:
		model = History 
		fields = (
			'id',
			'date',
			'status',
			'result',
			'job_id'
			)