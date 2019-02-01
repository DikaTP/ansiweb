# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import response, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from main import tasks
from main import models
from api import serializers
from api import permissions

class UserViewSet(viewsets.ModelViewSet):
 	queryset = models.User.objects.all()
	permission_classes = [IsAdminUser,]

	def get_serializer_class(self):

		if self.action == 'list':
			return serializers.UserListSerializer
		return serializers.UserSerializer

class CredentialViewSet(viewsets.ModelViewSet):
	queryset = models.Credential.objects.all()
	permission_classes = [permissions.IsOwnerOrAdmin,]

	def perform_create(self, serializer):

		serializer.save(user = self.request.user)

	def get_serializer_class(self):
		
		if self.request.method == 'GET':
			if self.action == 'list':
				return serializers.CredentialListSerializer
			return serializers.CredentialReadSerializer
		return serializers.CredentialSerializer

	def get_queryset(self):

		if self.action == 'list' and self.request.user.is_staff == False:
			user = self.request.user
			return models.Credential.objects.filter(user=user)
		else:
			return models.Credential.objects.all()

# class MachineCredentialViewSet(viewsets.ReadOnlyModelViewSet):
# 	queryset = models.MachineCredential.objects.all()
# 	serializer_class = serializers.MachineCredentialSerializer

# class AwsCredentialViewSet(viewsets.ReadOnlyModelViewSet):
# 	queryset = models.AwsCredential.objects.all()
# 	serializer_class = serializers.AwsCredentialSerializer

class InventoryViewSet(viewsets.ModelViewSet):
	queryset = models.Inventory.objects.all()
	permission_classes = [permissions.IsOwnerOrAdmin,]

	def perform_create(self, serializer):
		
		serializer.save(user = self.request.user)

	def get_serializer_class(self):

		if self.action == 'list':
			return serializers.InventoryListSerializer
		else:
			return serializers.InventorySerializer

	def get_queryset(self):

		if self.request.user.is_staff == False:
			user = self.request.user
			return models.Inventory.objects.filter(user=user)
		else:
			return models.Inventory.objects.all()

class PlaybookViewSet(viewsets.ModelViewSet):
	queryset = models.Playbook.objects.all()
	permission_classes = [permissions.IsOwnerOrAdmin,]
	
	def perform_create(self, serializer):

		serializer.save(user = self.request.user)

	def get_serializer_class(self):

		if self.action == 'list':
			return serializers.PlaybookListSerializer
		else:
			return serializers.PlaybookSerializer

	def get_queryset(self):

		if self.action == 'list' and self.request.user.is_staff == False:
			user = self.request.user
			return models.Playbook.objects.filter(user=user)
		else:
			return models.Playbook.objects.all()

class JobViewSet(viewsets.ModelViewSet):
	queryset = models.Job.objects.all()
	permission_classes = [permissions.IsOwnerOrAdmin,]

	def perform_create(self, serializer):

		serializer.save(user = self.request.user)

	def get_serializer_class(self):

		if self.request.method == 'GET':
			if self.action == 'list':
				return serializers.JobListSerializer
			return serializers.JobReadSerializer
		return serializers.JobSerializer

	def get_queryset(self):

		if self.action == 'list' and self.request.user.is_staff == False:
			user = self.request.user
			return models.Job.objects.filter(user=user)
		else:
			return models.Job.objects.all()

	@action(detail=True, methods=['post','get'], permission_classes=[permissions.IsOwnerOrAdmin,])
	def execute(self, request, pk=None):

		job = self.get_object()
		if not models.JobRunning.objects.filter(job=job).exists():
			tasks.run.delay(job.id)
			return response.Response('job is executed, check your job history for the result')
		else:
			return response.Response('job is still running, please wait till it done')

# class PlaybookJobViewSet(viewsets.ReadOnlyModelViewSet):
# 	queryset = models.PlaybookJob.objects.all()
# 	serializer_class = serializers.PlaybookJobSerializer

# class AdhocJobViewSet(viewsets.ReadOnlyModelViewSet):
# 	queryset = models.AdhocJob.objects.all()
# 	serializer_class = serializers.AdhocJobSerializer

class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.History.objects.all()
	serializer_class = serializers.HistorySerializer
	permission_classes = [permissions.IsJobOwnerForHistory,]

	def get_serializer_class(self):

		if self.action == 'list':
			return serializers.HistorySerializer
		else: return serializers.HistoryDetailSerializer

	def get_queryset(self):

		if self.action == 'list' and self.request.user.is_staff == False:
			user = self.request.user
			return models.History.objects.filter(job=models.Job.objects.filter(user=user))
		else:
			return models.History.objects.all()