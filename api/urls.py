from django.conf.urls import url

from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.include_format_suffixes = False
router.register('users', views.UserViewSet)
router.register('credentials', views.CredentialViewSet)
# router.register('machine-credential', views.MachineCredentialViewSet)
# router.register('aws-credential', views.AwsCredentialViewSet)
router.register('inventories', views.InventoryViewSet)
router.register('playbooks', views.PlaybookViewSet)
router.register('jobs', views.JobViewSet)
# router.register('playbook-jobs', views.PlaybookJobViewSet)
# router.register('adhoc-jobs', views.AdhocJobViewSet)
router.register('histories', views.HistoryViewSet)
# router.register('jobrunning', JobRunningViewSet)
urlpatterns = router.urls