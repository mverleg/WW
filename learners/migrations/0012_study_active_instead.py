# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

"""
	I keep refactoring this (I merged and undid quite some migrations) but I think I've got it now!
"""

class Migration(migrations.Migration):

    dependencies = [
        ('study', '0008_ordering'),
        ('learners', '0011_learner_reward_magnitude'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='learner',
            name='study_show_learn',
        ),
        migrations.AddField(
            model_name='learner',
            name='study_active',
            field=models.ForeignKey(related_name='current_learners', blank=True, to='study.ActiveTranslation', help_text=b'The current ActiveTranslation that is being asked and for which scores should be assigned.', null=True),
            preserve_default=True,
        ),
    ]
