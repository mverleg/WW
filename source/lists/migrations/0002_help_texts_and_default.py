# -*- coding: utf-8 -*-

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translationslist',
            name='name',
            field=models.CharField(help_text=b'What is this list called? E.g. "Chinese animal names"', max_length=48),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='translationslist',
            name='public',
            field=models.BooleanField(default=True, help_text=b'Can anyone follow this list?'),
            preserve_default=True,
        ),
    ]
