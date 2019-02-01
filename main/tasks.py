from __future__ import absolute_import, unicode_literals
from celery import shared_task
import subprocess
from datetime import datetime, timedelta
from main import models
from django.conf import settings

@shared_task
def run(job_id):
	job = models.Job.objects.get(pk=job_id)
	running = models.JobRunning(job=job)
	history = models.History(status='STARTED', result='', job=job)
	history.save()
	running.save()
	base_folder = settings.MEDIA_URL
	inv_path = '{0}{1}'.format(base_folder, job.inventory.file.name)
	verbosity = job.verbosity
	ssh_username = job.credential.machine_detail.ssh_username
	ssh_pass = job.credential.machine_detail.ssh_pass
	privilege_flag = job.privilege_flag

	if job.job_type == 'pb':
		pb_path = '{0}{1}'.format(base_folder, job.playbook_detail.playbook.file.name)
		if privilege_flag is True:
			privilege_pass = job.credential.machine_detail.privilege_pass
			cmd = 'ansible-playbook {0} -i {1} -e\"ansible_user={2} ansible_ssh_pass={3} ansible_become={4} ansible_become_pass={5}\" {6}'.format(
				pb_path,
				inv_path,
				ssh_username,
				ssh_pass,
				privilege_flag,
				privilege_pass,
				verbosity
				)
		else:
			cmd = 'ansible-playbook {0} -i {1} -e\"ansible_user={2} ansible_ssh_pass={3}\" {4}'.format(
				pb_path,
				inv_path,
				ssh_username,
				ssh_pass,
				verbosity
				)
	else:
		module = job.adhoc_detail.module
		arguments = job.adhoc_detail.arguments

		if arguments == '':
			arguments = ''
		else:
			arguments = '-a\"{0}\"'.format(arguments)

		if privilege_flag is True:
			privilege_pass = job.credential.machine_detail.privilege_pass
			cmd = 'ansible all -m {0} -i {1} {2} -e\"ansible_user={3} ansible_ssh_pass={4} ansible_become={5} ansible_become_pass={6}\" {7}'.format(
				module,
				inv_path,
				arguments,
				ssh_username,
				ssh_pass,
				privilege_flag,
				privilege_pass,
				verbosity
				)
		else:
			cmd = 'ansible all -m {0} -i {1} {2} -e\"ansible_user={3} ansible_ssh_pass={4}\" {5}'.format(
				module,
				inv_path,
				arguments,
				ssh_username,
				ssh_pass,
				verbosity
				)

	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	stdout, stderr = p.communicate()
	models.JobRunning.objects.get(pk=running.id).delete()
	tz_info = history.date.tzinfo
	history.status = 'COMPLETED'
	history.result = stdout.replace("\n", "").replace("*", "").replace("\"", "")
	avg = datetime.now(tz_info) - history.date
	avg = avg - timedelta(microseconds=avg.microseconds)
	history.runtime = avg
	history.save()