from __future__ import absolute_import, unicode_literals
from celery import shared_task
import subprocess, sys

@shared_task
def run_playbook(playbook_source, inventory_source):
    cmd = "ansible-playbook {} -i {}".format(playbook_source, inventory_source)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    return stdout