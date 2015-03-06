# -*- coding: utf-8 -*-

"""
	This is for database upgrades, you can ignore it and preferably don't change anything.
"""

from __future__ import unicode_literals
from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

	dependencies = [
		('auth', '0001_initial'),
	]

	operations = [
		migrations.CreateModel(
			name='Learner',
			fields=[
				('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
				('password', models.CharField(max_length=128, verbose_name='password')),
				('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
				('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
				('email', models.EmailField(help_text=b'Email address; also used as login name.', unique=True, max_length=254, blank=True)),
				('name', models.CharField(help_text=b'Visible name on the site.', max_length=48, blank=True)),
				('is_staff', models.BooleanField(default=False, help_text=b'Designates whether the user can log into this admin site.')),
				('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
				('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
			],
			options={
			},
			bases=(models.Model,),
		),
	]
