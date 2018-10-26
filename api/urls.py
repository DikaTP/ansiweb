from django.conf.urls import url

from views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('jobs', JobViewSet)
router.register('inventories', InventoryViewSet)
router.register('playbooks', PlaybookViewSet)

urlpatterns = [
	url(r'^run', execute)
] + router.urls