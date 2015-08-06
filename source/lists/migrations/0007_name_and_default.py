# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0006_phrase_to_translation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='translationslist',
            options={'verbose_name': 'list'},
        ),
        migrations.AlterField(
            model_name='translationslist',
            name='translations',
            field=models.ManyToManyField(related_name='lists', to='phrasebook.Translation', blank=True),
            preserve_default=True,
        ),
    ]
