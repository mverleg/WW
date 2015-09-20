# -*- coding: utf-8 -*-

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('learners', '0005_learner_need_active_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='learner',
            name='ask_direction',
            field=models.FloatField(default=65, help_text=b'How often to show the known language and ask the unknown one, versus the other way around (0: always show unknown, 100: always show known)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
            preserve_default=True,
        ),
    ]
