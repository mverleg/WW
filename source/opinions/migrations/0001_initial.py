# -*- coding: utf-8 -*-

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('phrasebook', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TranslationComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('learner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('translation', models.ForeignKey(related_name='comments', to='phrasebook.Translation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TranslationVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('up', models.BooleanField(default=True, help_text=b"Is this an upvote? (Otherwise it's a downvote)")),
                ('learner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('translation', models.ForeignKey(related_name='votes', to='phrasebook.Translation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
