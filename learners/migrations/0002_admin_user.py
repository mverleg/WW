# -*- coding: utf-8 -*-

"""
	This is for database upgrades, you can ignore it and preferably don't change anything.
"""

from __future__ import unicode_literals
from sys import stderr
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager
from django.db import migrations


def create_admin(apps, schema_editor):
	Learner = apps.get_model('learners', 'Learner')
	email = BaseUserManager.normalize_email('admin@localhost')
	admin = Learner(email = email, is_staff = True, is_superuser = True)
	admin.name = 'Admin'
	admin.need_active_update = True
	admin.minimum_delay = 3
	admin.new_count = 5
	admin.password = make_password('MCTDH')
	admin.save()
	stderr.write('\n*********************************************************************\nA user with email "admin@localhost" and password "MCTDH" was created.\nYou should update the password!\n*********************************************************************\n')


class Migration(migrations.Migration):

	dependencies = [
		('learners', '0001_initial'),
	]

	operations = [
		migrations.RunPython(create_admin)
	]


