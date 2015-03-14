# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phrasebook', '0003_phrase_public_view'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phrase',
            name='public_edit',
            field=models.BooleanField(default=True, verbose_name=b'publicly editable'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='phrase',
            name='public_view',
            field=models.BooleanField(default=True, verbose_name=b'publicly viewable'),
            preserve_default=True,
        ),
    ]
