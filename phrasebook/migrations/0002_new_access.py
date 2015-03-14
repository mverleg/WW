# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
	At this point I reverted a bunch of migrations, a.o. removing view permission for phrases.
"""

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('phrasebook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='phrase',
            name='learner',
            field=models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='phrase',
            name='public_edit',
            field=models.BooleanField(default=True, verbose_name=b'publicly editable'),
            preserve_default=True,
        ),
    ]
