# -*- coding: utf-8 -*-

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('phrasebook', '0002_new_access'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=8, choices=[(b'en-gb', 'English (British)'), (b'zh-cn', 'Chinese (simplified Mandarin)'), (b'de', 'German'), (b'nl', 'Dutch')])),
                ('result', models.CharField(max_length=12, choices=[(b'good', b'correct'), (b'bad', b'incorrect'), (b'kinda', b'not quite correct')])),
                ('learner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('translation', models.ForeignKey(to='phrasebook.Translation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
