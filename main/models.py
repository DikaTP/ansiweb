# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
	AbstractBaseUser,
	BaseUserManager,
	PermissionsMixin
)

class UserManager(BaseUserManager):
	def create_user(self, username, password, email, active=True, is_staff=False, is_admin=False):
		if not username:
			raise ValueError("User must have an username")
		if not password:
			raise ValueError("Users must have a password")
		if not email:
			raise ValueError("Users must have an email address")
		user_obj.username = username
		user_obj.set_password(password)
		user_obj = self.model(
			email = self.normalize_email(email)
		)
		user_obj.active = is_active
		user_obj.staff = is_staff
		user_obj.admin = is_admin
		user_obj.save(using=self._db)
		return user_obj

	def create_staffuser(self, username, password, email):
		user = self.create_user(
			username,
			password,			
			email,
			)
		user.staff=True
		return user

	def create_superuser(self, username, password, email):
		user = self.create_user(
			username,			
			password,
			email,
			)
		user.admin=True
		return user

class User(AbstractBaseUser):
	username = models.CharField(max_length=128, unique=True)
	email = models.EmailField(max_length=128, unique=True)	
	first_name = models.CharField(max_length=128, blank=True, null=True)
	last_name = models.CharField(max_length=128, blank=True, null=True)
	active = models.BooleanField(default=True)
	staff = models.BooleanField(default=False)
	admin = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELD = ['email']

	objects = UserManager()

	def __str__(self):
		return username

	def get_full_name(self):
		full_name = '{} {}'.format(first_name, last_name)
		return full_name

	def get_short_name(self):
		return self.first_name

	@property
	def is_staff(self):
		return self.staff

	@property
	def is_admin(self):
		return self.admin

	@property
	def is_active(self):
		return self.active

def cred_dir_path(instance, filename):
	return 'user_{0}/credentials/{1}'.format(instance.owner.username, filename)

def inv_dir_path(instance, filename):
	return 'user_{0}/inventories/{1}'.format(instance.owner.username, filename)

def pb_dir_path(instance, filename):
	return 'user_{0}/playbooks/{1}'.format(instance.owner.username, filename)

class Credential(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='credentials', on_delete=models.CASCADE)
	description = models.TextField()
	file = models.FileField(upload_to=cred_dir_path, default='settings.MEDIA_ROOT/None/no-file.txt')
	uploaded_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.file.name

	def __unicode__(self):
		return self.file.name

class Inventory(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='inventories', on_delete=models.CASCADE)
	description = models.TextField()
	file = models.FileField(upload_to=inv_dir_path, default='settings.MEDIA_ROOT/None/no-file.txt')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.description

	def __unicode__(self):
		return self.file.name

class Playbook(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='playbooks', on_delete=models.CASCADE)
	description = models.TextField()
	file = models.FileField(upload_to=pb_dir_path, default='settings.MEDIA_ROOT/None/no-file.txt')
	uploaded_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.description

	def __unicode__(self):
		return self.file.name

class Job(models.Model):
	name = models.CharField(max_length=128, unique=True)
	description = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='jobs', on_delete=models.CASCADE)
	playbook = models.ForeignKey(Playbook, related_name='playbook', on_delete=models.CASCADE)
	inventory = models.ForeignKey(Inventory, related_name='inventory', on_delete=models.CASCADE)

	def __str__(self):
		return self.name

	def __unicode__(self):
		return self.name

class History(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=128)
	result = models.TextField()
	job_id = models.ForeignKey(Job, on_delete=models.CASCADE)

	def __str__(self):
		return self.status

	def __unicode__(self):
		return self.status

	class Meta:
		ordering = ('date',)