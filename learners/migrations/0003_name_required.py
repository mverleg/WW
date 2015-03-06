# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learners', '0002_admin_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learner',
            name='name',
            field=models.CharField(help_text=b'Visible name on the site.', max_length=48),
            preserve_default=True,
        ),
    ]
