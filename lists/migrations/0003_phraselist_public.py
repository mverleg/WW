# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0002_auto_20150306_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='phraselist',
            name='public',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
