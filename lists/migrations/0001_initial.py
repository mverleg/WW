# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('phrasebook', '0002_translation_phrase'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListAccess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('access', models.CharField(max_length=4, choices=[(b'view', b'view list'), (b'edit', b'edit list')])),
                ('priority', models.SmallIntegerField(default=0)),
                ('active', models.BooleanField(default=False)),
                ('learner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ListEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phrase', models.ForeignKey(to='phrasebook.Phrase')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhraseList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=48)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='listentry',
            name='phrase_list',
            field=models.ForeignKey(to='lists.PhraseList'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='listaccess',
            name='phrase_list',
            field=models.ForeignKey(to='lists.PhraseList'),
            preserve_default=True,
        ),
    ]
