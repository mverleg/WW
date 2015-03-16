# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learners', '0007_show_stats_setting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learner',
            name='phrase_index',
            field=models.PositiveIntegerField(default=100, help_text=b'How many phrases have been shown (a.o. to compare last_shown) (internal only).'),
            preserve_default=True,
        ),
    ]
