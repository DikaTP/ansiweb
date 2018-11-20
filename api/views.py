# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework import viewsets
from main import tasks
from django.shortcuts import render
from main.models import *
from serializers import *

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class JobViewSet(viewsets.ModelViewSet):
	queryset = Job.objects.all()
	serializer_class = JobSerializer

	@action(detail=True, methods=['get'])
	def execute(self, request, pk=None):
		job = self.get_object()
		if not JobRunning.objects.filter(job=job).exists():
			base_folder = settings.MEDIA_URL
			pb = '{0}{1}'.format(base_folder, job.playbook.file.name)
			inv = '{0}{1}'.format(base_folder, job.inventory.file.name)
			t = tasks.run_playbook.delay(pb, 'localhost',job.id)
			return response.Response('job is executed, check your job history for the result')	
		else:
			return response.Response('job is still running')

# class CredentialViewSet(viewsets.ModelViewSet):#buat fungsi delete file lama kalo model di delete atau abis update file baru(PUT)
# 	queryset = Credential.objects.all()        #CUMAN PERLU CREATE, RETRIEVE, DELETE
# 	serializer_class = CredentialSerializer

class InventoryViewSet(viewsets.ModelViewSet): #buat fungsi delete file lama kalo model di delete atau abis update file baru(PUT)
	queryset = Inventory.objects.all()			#CUMAN PERLU CREATE, RETRIEVE, DELETE
	serializer_class = InventorySerializer

class PlaybookViewSet(viewsets.ModelViewSet): #buat fungsi delete file lama kalo model di delete atau abis update file baru(PUT)
	queryset = Playbook.objects.all()			#CUMAN PERLU CREATE, RETRIEVE, DELETE
	serializer_class = PlaybookSerializer

class HistoryViewSet(viewsets.ModelViewSet):
	queryset = History.objects.all()
	serializer_class = HistorySerializer

class JobRunningViewSet(viewsets.ModelViewSet):
	queryset = JobRunning.objects.all()
	serializer_class = JobRunningSerializer