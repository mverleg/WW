# -*- coding: utf-8 -*-

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phrasebook', '0002_new_access'),
        ('study', '0002_result_when'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='language',
        ),
        migrations.RemoveField(
            model_name='result',
            name='translation',
        ),
        migrations.AddField(
            model_name='result',
            name='asked',
            field=models.ForeignKey(related_name='results_asked', default=1, to='phrasebook.Translation', help_text=b'The translation that was asked for (in presumably the target language)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='known',
            field=models.ForeignKey(related_name='results_known', default=1, to='phrasebook.Translation', help_text=b'The translation that was shown (in presumably known language)'),
            preserve_default=False,
        ),
    ]
