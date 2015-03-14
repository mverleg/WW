# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phrasebook', '0002_phrase_access'),
    ]

    operations = [
        migrations.AddField(
            model_name='phrase',
            name='public_view',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
