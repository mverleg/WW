# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learners', '0010_admin_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='learner',
            name='reward_magnitude',
            field=models.IntegerField(default=10, help_text=b"Indicates the base magnitude or increase or decrease for a phrase's score when correct or incorrect."),
            preserve_default=True,
        ),
    ]
