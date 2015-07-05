# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0008_initial_lists'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='listaccess',
            unique_together=set([('translations_list', 'learner')]),
        ),
    ]
