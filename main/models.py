# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import (
	AbstractBaseUser,
	BaseUserManager,
	PermissionsMixin
)


class UserManager(BaseUserManager):

	def create_user(self, username, email, name, password=None):

		if not username:
			raise ValueError('username cannot be empty')
		if not email:
			raise ValueError('email cannot be empty')
		if not name:
			raise ValueError('name cannot be empty')
		if not password:
			raise ValueError('password cannot be empty')

		email = self.normalize_email(email)
		user = self.model(
			username = username,
			email = email,
			name = name
			)

		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, username, email, name, password):

		user = self.create_user(username, email, name, password)

		user.is_superuser = True
		user.is_staff = True
		user.save(using=self._db)

		return user

class User(AbstractBaseUser, PermissionsMixin):

	username = models.CharField(max_length=32, unique=True)
	email = models.EmailField(max_length=64, unique=True)
	name = models.CharField(max_length=64)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email', 'name']

	def get_short_name():
		return self.name

	def __str__(self):
		return self.username

	def get_absolute_url(self):
		return reverse('api:user-detail', kwargs={'pk': self.pk})

def inv_dir_path(instance, filename):
	return 'user_{0}/inventories/{1}'.format(instance.user.username, filename)

def pb_dir_path(instance, filename):
	return 'user_{0}/playbooks/{1}'.format(instance.user.username, filename)

class Credential(models.Model):

	CRED_TYPES = (
		('machine', 'Machine'),
		('aws', 'Amazon Web Services')
	)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='credentials', on_delete=models.CASCADE)
	name = models.CharField(max_length=32)
	description = models.TextField(blank=True)
	credential_type = models.CharField(max_length=32, choices=CRED_TYPES, default='machine')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	REQUIRED_FIELDS = ['name',]

	def __str__(self):
		return self.name

	def __unicode__(self):
		return self.name

	@property
	def owner(self):
		return self.user

	def get_absolute_url(self):
		return reverse('api:credential-detail', kwargs={'pk': self.pk})

class MachineCredential(models.Model):

	credential = models.OneToOneField(Credential, related_name = 'machine_detail')
	ssh_username = models.CharField(max_length=32, default='')
	ssh_pass = models.CharField(max_length=32, default='')
	privilege_pass = models.CharField(max_length=32, default='')

	REQUIRED_FIELDS = ['ssh_username', 'ssh_pass', 'privilege_pass']

class AwsCredential(models.Model):

	credential = models.OneToOneField(Credential, related_name = 'aws_detail')
	access_key = models.CharField(max_length=64, default='')
	secret_access_key = models.CharField(max_length=64, default='')

	REQUIRED_FIELDS = ['access_key', 'secret_access_key']


class Inventory(models.Model):

	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='inventories', on_delete=models.CASCADE)
	description = models.CharField(max_length=64 ,blank=True)
	file = models.FileField(upload_to=inv_dir_path, default='settings.MEDIA_ROOT/None/no-file.txt')
	uploaded_at = models.DateTimeField(auto_now_add=True)


	REQUIRED_FIELDS = ['file', 'description']
	
	def __str__(self):
		return self.description

	def __unicode__(self):
		return self.file.name

	@property
	def owner(self):
		return self.user

	def get_absolute_url(self):
		return reverse('api:inventory-detail', kwargs={'pk': self.pk})

class Playbook(models.Model):

	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='playbooks', on_delete=models.CASCADE)
	description = models.CharField(max_length=64 ,blank=True)
	file = models.FileField(upload_to=pb_dir_path, default='settings.MEDIA_ROOT/None/no-file.txt')
	uploaded_at = models.DateTimeField(auto_now_add=True)

	REQUIRED_FIELDS = ['file', 'description']

	def __str__(self):
		return self.description

	def __unicode__(self):
		return self.file.name

	@property
	def owner(self):
		return self.user

	def get_absolute_url(self):
		return reverse('api:playbook-detail', kwargs={'pk': self.pk})

class Job(models.Model):

	NORMAL = ' '
	LEVEL1 = '-v'
	LEVEL2 = '-vv'
	LEVEL3 = '-vvv'
	VERBOSITY_CHOICES = (
		(NORMAL, 'Normal'),
		(LEVEL1, 'Level 1'),
		(LEVEL2, 'Level 2'),
		(LEVEL3, 'Level 3'),
	)

	JOB_TYPES = (
		('pb', 'Playbook'),
		('adhoc', 'Adhoc')
		)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='jobs', on_delete=models.CASCADE)
	inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
	credential = models.ForeignKey(Credential, on_delete=models.CASCADE)
	name = models.CharField(max_length=64, unique=True)
	description = models.CharField(max_length=64 ,blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	verbosity = models.CharField(max_length=8, choices=VERBOSITY_CHOICES, default=NORMAL)
	privilege_flag = models.BooleanField(default=False)
	job_type = models.CharField(max_length=8, choices=JOB_TYPES, default='pb')

	REQUIRED_FIELDS = ['inventory', 'credential', 'name']

	def __str__(self):
		return self.name

	def __unicode__(self):
		return self.name

	@property
	def owner(self):
		return self.user

	def get_absolute_url(self):
		return reverse('api:job-detail', kwargs={'pk': self.pk})

class PlaybookJob(models.Model):

	job = models.OneToOneField(Job, related_name='playbook_detail')
	playbook = models.ForeignKey(Playbook, on_delete=models.CASCADE)

class AdhocJob(models.Model):

	MODULE_CHOICES = (
		('shell', 'shell'),
		('yum', 'yum'),
		('apt', 'apt'),
		('command', 'command'),
		('ping', 'ping'),
	)

	job = models.OneToOneField(Job, related_name='adhoc_detail')
	module = models.CharField(max_length=8, choices=MODULE_CHOICES, default='shell')
	arguments = models.CharField(max_length=128, default='')

	REQUIRED_FIELDS = ['module', 'arguments']

class History(models.Model):

	date = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=32,blank=True)
	result = models.TextField(blank=True)
	job = models.ForeignKey(Job, on_delete=models.CASCADE)
	runtime = models.DurationField(blank=True, null=True)

	def __str__(self):
		return self.status

	def __unicode__(self):
		return self.status

	def get_absolute_url(self):
		return reverse('api:history-detail', kwargs={'pk': self.pk})

class JobRunning(models.Model):

	job = models.ForeignKey(Job, on_delete=models.CASCADE)


