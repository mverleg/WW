# -*- coding: utf-8 -*-

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learners', '0004_learner_show_medium_correctness'),
    ]

    operations = [
        migrations.AddField(
            model_name='learner',
            name='need_active_update',
            field=models.BooleanField(default=True, help_text=b'Do the cache fields on active phrases need updating? (internal only)'),
            preserve_default=True,
        ),
    ]
