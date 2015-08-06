# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('learners', '0006_learner_ask_direction'),
    ]

    operations = [
        migrations.AddField(
            model_name='learner',
            name='show_correct_count',
            field=models.BooleanField(default=True, help_text=b'Show the number of correct responses on every page.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='learner',
            name='ask_direction',
            field=models.FloatField(default=65, help_text=b'How often to show the known language and ask the unknown one, versus the other way around (0: always show unknown, 100: always show known).', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='learner',
            name='need_active_update',
            field=models.BooleanField(default=True, help_text=b'Do the cache fields on active phrases need updating? (internal only).'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='learner',
            name='phrase_index',
            field=models.IntegerField(default=0, help_text=b'How many phrases have been shown (a.o. to compare last_shown) (internal only).'),
            preserve_default=True,
        ),
    ]
