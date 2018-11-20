from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.result import AsyncResult
import subprocess, sys
from main import models

@shared_task
def run_playbook(playbook_source, inventory_source, credential, job_id):
	job = models.Job.objects.get(pk=job_id)
	running = models.JobRunning(job=job)
	history = models.History(status='STARTED', result='', job=job)
	running.save()
	history.save()
	cmd = "ansible-playbook {} -i {}".format(playbook_source, inventory_source)
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	stdout, stderr = p.communicate()
	models.JobRunning.objects.get(pk=running.id).delete()
	history.status = 'COMPLETED'
	history.result = stdout
	history.save()
	return stdout
