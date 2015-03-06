# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phrasebook', '0002_translation_phrase'),
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listentry',
            name='phrase',
        ),
        migrations.RemoveField(
            model_name='listentry',
            name='phrase_list',
        ),
        migrations.DeleteModel(
            name='ListEntry',
        ),
        migrations.AlterModelOptions(
            name='listaccess',
            options={'ordering': ('-priority',)},
        ),
        migrations.AddField(
            model_name='phraselist',
            name='phrases',
            field=models.ManyToManyField(related_name='lists', to='phrasebook.Phrase'),
            preserve_default=True,
        ),
    ]
