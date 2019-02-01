# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.User)
admin.site.register(models.Credential)
admin.site.register(models.Inventory)
admin.site.register(models.Playbook)
admin.site.register(models.Job)
admin.site.register(models.PlaybookJob)
admin.site.register(models.AdhocJob)