# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0004_active_translations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='result',
            field=models.SmallIntegerField(choices=[(1, b'correct'), (-2, b'incorrect'), (-1, b'not quite correct')]),
            preserve_default=True,
        ),
    ]
