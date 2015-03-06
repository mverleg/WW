# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phrasebook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='translation',
            name='phrase',
            field=models.ForeignKey(related_name='translations', default=1, to='phrasebook.Phrase'),
            preserve_default=False,
        ),
    ]
