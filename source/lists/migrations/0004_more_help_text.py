# -*- coding: utf-8 -*-

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_rename_translations_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listaccess',
            name='active',
            field=models.BooleanField(default=False, help_text=b"Inactive lists don't show up during learning sessions (only applies to you)."),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='listaccess',
            name='priority',
            field=models.SmallIntegerField(default=0, help_text=b'Higher priority lists will show up more during learning sessions (only applies to you).'),
            preserve_default=True,
        ),
    ]
