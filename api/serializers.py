from rest_framework import serializers
from main.models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
	jobs = serializers.SlugRelatedField(many=True, read_only=True, slug_field = 'name')
	
	class Meta:
		model = User
		fields = (
			'id', 
			'username',
			'password', 
			'jobs',)

class JobSerializer(serializers.ModelSerializer):
	inventory = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	playbook = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

	class Meta:
		model = Job
		fields = (
			'id',
			'name',
			'owner', 
			'description',
			'inventory', 
			'playbook', 
			'created_at', 
			)

class InventorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Inventory 
		fields = (
			'id', 
			'description', 
			'path', 
			'uploaded_at', 
			'job_id',)

class PlaybookSerializer(serializers.ModelSerializer):
	class Meta:
		model = Playbook 
		fields = (
			'id', 
			'description', 
			'path', 
			'uploaded_at', 
			'job_id',)