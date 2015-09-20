# -*- coding: utf-8 -*-

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learners', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='learner',
            name='add_randomness',
            field=models.BooleanField(default=True, help_text=b'Should selecting phrases involve a little randomness?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='learner',
            name='minimum_delay',
            field=models.PositiveIntegerField(default=10, help_text=b'For how many questions to block a phrase after displaying it.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='learner',
            name='new_count',
            field=models.PositiveIntegerField(default=10, help_text=b'How many unlearned translations to keep active at once.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='learner',
            name='phrase_index',
            field=models.IntegerField(default=0, help_text=b'How many phrases have been shown (a.o. to compare last_shown) (internal only)'),
            preserve_default=True,
        ),
    ]
