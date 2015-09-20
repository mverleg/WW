# -*- coding: utf-8 -*-

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Phrase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=8, choices=[(b'en-gb', 'English (British)'), (b'zh-cn', 'Chinese (simplified Mandarin)'), (b'de', 'German'), (b'nl', 'Dutch')])),
                ('text', models.TextField()),
                ('phrase', models.ForeignKey(related_name='translations', to='phrasebook.Phrase')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
