# -*- coding: utf-8 -*-

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opinions', '0002_unicity_constraint'),
    ]

    operations = [
        migrations.AddField(
            model_name='translationvote',
            name='value',
            field=models.SmallIntegerField(default=1, help_text=b"Automatic field, don't edit! +1 for up, -1 for down"),
            preserve_default=False,
        ),
    ]
