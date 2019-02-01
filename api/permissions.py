from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):

	def check_object_permission(self, user, obj):
		return (user and user.is_authenticated() and (user.is_staff or obj.user == user))

	def has_object_permission(self, request, view, obj):
		return self.check_object_permission(request.user, obj)

	def has_permission(self, request, view):
		return request.user and request.user.is_authenticated()

class IsJobOwnerForHistory(permissions.BasePermission):

	def check_object_permission(self, user, obj):
		return (user and user.is_authenticated() and (user.is_staff or obj.job.user == user))

	def has_object_permission(self, request, view, obj):
		return self.check_object_permission(request.user, obj)

	def has_permission(self, request, view):
		return request.user and request.user.is_authenticated()