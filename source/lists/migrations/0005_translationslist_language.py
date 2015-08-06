# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_more_help_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='translationslist',
            name='language',
            field=models.CharField(blank=True, max_length=8, null=True, help_text=b'You can select the language to learn for this list, or leave it blank for a mixed-language list.', choices=[(b'en-gb', 'English (British)'), (b'zh-cn', 'Chinese (simplified Mandarin)'), (b'de', 'German'), (b'nl', 'Dutch')]),
            preserve_default=True,
        ),
    ]
