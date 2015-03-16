# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0006_more_caching_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='verified',
            field=models.BooleanField(default=False, help_text=b'True if the user typed the solution correctly, False otherwise (if he judged himself)'),
            preserve_default=True,
        ),
    ]
