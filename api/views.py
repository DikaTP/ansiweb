# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import response, status
from rest_framework.decorators import action, api_view
from rest_framework.parsers import FileUploadParser
from rest_framework import viewsets
from main.tasks import run_ansible
from django.shortcuts import render
from main.models import *
from serializers import *
from django.contrib.auth.models import User

import json
# Create your views here.


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
			return response.Response(serializer.data)
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
			return response.Response(serializer.data)
		return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def execute(request):
	t = run_ansible.delay('upload/playbooks/get_ip.yml', 'localhost')
	while t.status == 'SUCCESS':
		return response.Response({'result': t.get(timeout=7)})
	return response.Response({'result': t.get(timeout=7)})