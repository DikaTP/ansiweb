# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Job(models.Model):
	name = models.CharField(max_length=128)
	owner = models.ForeignKey(User, related_name='jobs', on_delete=models.CASCADE)
	description = models.CharField(max_length=128)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

#def project_path(instance, filename):
#	return 'job_{1}/{2}'.format(instance.for_job.id, filename)

class Inventory(models.Model):
	description = models.CharField(max_length=50)
	path = models.FileField(upload_to='inventories')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	job_id = models.ForeignKey(Job, related_name='inventory', on_delete=models.CASCADE)

	def __str__(self):
		return self.path

class Playbook(models.Model):
	description = models.CharField(max_length=50)
	path = models.FileField(upload_to='playbooks')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	job_id = models.ForeignKey(Job, related_name='playbook', on_delete=models.CASCADE)

	def __str__(self):
		return self.path
