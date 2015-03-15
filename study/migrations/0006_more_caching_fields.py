# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0005_result_integer'),
    ]

    operations = [
        migrations.AddField(
            model_name='activetranslation',
            name='active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activetranslation',
            name='priority',
            field=models.SmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
