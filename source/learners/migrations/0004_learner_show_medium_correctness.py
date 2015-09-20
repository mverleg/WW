# -*- coding: utf-8 -*-

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learners', '0003_study_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='learner',
            name='show_medium_correctness',
            field=models.BooleanField(default=False, help_text=b'Besides correct and incorrect, show a third option inbetween them.'),
            preserve_default=True,
        ),
    ]
