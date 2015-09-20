# -*- coding: utf-8 -*-

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0002_help_texts_and_default'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listaccess',
            old_name='translation_list',
            new_name='translations_list',
        ),
    ]
