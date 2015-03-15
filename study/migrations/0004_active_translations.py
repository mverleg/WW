# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('phrasebook', '0002_new_access'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('study', '0003_known_translation'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_shown', models.PositiveIntegerField()),
                ('score', models.FloatField()),
                ('learner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('translation', models.ForeignKey(to='phrasebook.Translation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='activetranslation',
            unique_together=set([('learner', 'translation')]),
        ),
        migrations.AlterModelOptions(
            name='result',
            options={'ordering': ('when',)},
        ),
    ]
