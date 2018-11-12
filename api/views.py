# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from rest_framework import response, status
from rest_framework.decorators import action, api_view
from rest_framework.parsers import FileUploadParser
from rest_framework import viewsets
from main.tasks import run_playbook
from django.shortcuts import render
from main.models import *
from serializers import *

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class JobViewSet(viewsets.ModelViewSet):
	queryset = Job.objects.all()
	serializer_class = JobSerializer

	@action(detail=True, methods=['post','get'])
	def execute(self, request, pk=None):
		job = self.get_object()
		base_folder = settings.MEDIA_URL
		pb = '{0}{1}'.format(base_folder, job.playbook.file.name)
		inv = '{0}{1}'.format(base_folder, job.inventory.file.name)
		t = run_playbook.delay(pb, 'localhost')
		return response.Response(t.get(timeout=10))

class CredentialViewSet(viewsets.ModelViewSet):#buat fungsi delete file lama kalo model di delete atau abis update file baru(PUT)
	queryset = Credential.objects.all()        #CUMAN PERLU CREATE, RETRIEVE, DELETE
	serializer_class = CredentialSerializer

class InventoryViewSet(viewsets.ModelViewSet): #buat fungsi delete file lama kalo model di delete atau abis update file baru(PUT)
	queryset = Inventory.objects.all()			#CUMAN PERLU CREATE, RETRIEVE, DELETE
	serializer_class = InventorySerializer

class PlaybookViewSet(viewsets.ModelViewSet): #buat fungsi delete file lama kalo model di delete atau abis update file baru(PUT)
	queryset = Playbook.objects.all()			#CUMAN PERLU CREATE, RETRIEVE, DELETE
	serializer_class = PlaybookSerializer

class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = History.objects.all()
	serializer_class = HistorySerializer
