# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('learners', '0012_study_active_instead'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='learner',
            name='add_randomness',
        ),
        migrations.AddField(
            model_name='learner',
            name='favor_unknown',
            field=models.FloatField(default=10, help_text=b'A higher value makes unknown phrases more likely to appear during study sessions, relative to known ones.', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
            preserve_default=True,
        ),
    ]
