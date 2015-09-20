# -*- coding: utf-8 -*-

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opinions', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='translationvote',
            unique_together=set([('translation', 'learner')]),
        ),
    ]
