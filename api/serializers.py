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

class CredentialSerializer(serializers.ModelSerializer):

	file = serializers.FileField(allow_empty_file=False, use_url=False)

	class Meta:
		model = Inventory
		fields = (
			'id',
			'description', 
			'file', 
			'uploaded_at', 
			'owner',
			)

class InventorySerializer(serializers.ModelSerializer):

	file = serializers.FileField(allow_empty_file=False, use_url=False)

	class Meta:
		model = Inventory 
		fields = (
			'id',
			'description', 
			'file', 
			'uploaded_at', 
			'owner',
			)

class PlaybookSerializer(serializers.ModelSerializer):

	file = serializers.FileField(allow_empty_file=False, use_url=False)

	class Meta:
		model = Playbook 
		fields = (
			'id', 
			'description', 
			'file', 
			'uploaded_at', 
			'owner',
			)


class JobSerializer(serializers.ModelSerializer):

	class Meta:
		model = Job
		fields = (
			'id',
			'name',
			'description', 
			'created_at',
			'owner',
			'playbook',
			'inventory'
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