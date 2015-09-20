# -*- coding: utf-8 -*-

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0007_result_verified'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='result',
            options={'ordering': ('-when',)},
        ),
        migrations.AlterModelOptions(
            name='activetranslation',
            options={'ordering': ('score',)},
        ),
    ]
