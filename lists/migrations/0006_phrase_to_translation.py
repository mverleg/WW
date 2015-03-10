# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phrasebook', '0001_initial'),
        ('lists', '0005_translationslist_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='translationslist',
            name='phrases',
        ),
        migrations.AddField(
            model_name='translationslist',
            name='translations',
            field=models.ManyToManyField(related_name='lists', to='phrasebook.Translation'),
            preserve_default=True,
        ),
    ]
