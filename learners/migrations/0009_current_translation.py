# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0007_result_verified'),
        ('learners', '0008_min_delay_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='learner',
            name='learn_translation',
            field=models.ForeignKey(related_name='current_learners', default=None, blank=True, to='study.ActiveTranslation', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='learner',
            name='is_revealed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
