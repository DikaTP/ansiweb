# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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

class InventoryViewSet(viewsets.ModelViewSet):
	queryset = Inventory.objects.all()
	serializer_class = InventorySerializer

	@action(
		detail = True,
		methods = ['PUT'],
		parser_classes = [FileUploadParser],)

	def upload(self, request, pk):
		obj = self.get_object()
		serializer = self.serializer_class(obj, data=request.data, partial=True)

		if serializer.is_valid():
			serializer.save()
			return response.Response(serializer.data, status.HTTP_201_CREATED)
		return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class PlaybookViewSet(viewsets.ModelViewSet):
	queryset = Playbook.objects.all()
	serializer_class = PlaybookSerializer

	@action(
		detail = True,
		methods = ['PUT'],
		parser_classes = [FileUploadParser],)

	def upload(self, request, pk):
		obj = self.get_object()
		serializer = self.serializer_class(obj, data=request.data, partial=True)

		if serializer.is_valid():
			serializer.save()
			return response.Response(serializer.data, status.HTTP_201_CREATED)
		return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = History.objects.all()
	serializer_class = HistorySerializer

@api_view(['GET'])
def execute(request):
	t = run_playbook.delay('upload/playbooks/get_ip.yml', 'localhost')
	while t.status == 'SUCCESS':
		return response.Response({'result': t.get()})
	return response.Response({'result': t.get()})