# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

	dependencies = [
		('study', '0007_result_verified'),
		('learners', '0008_min_delay_default'),
	]

	operations = [
		migrations.AddField(
			model_name='learner',
			name='study_state',
			field=models.PositiveSmallIntegerField(default=1, help_text=b'(internal only).', choices=[(1, b'asking meaning (showing learn lang)'), (2, b'asking how to say (showing known lang)'), (3, b'revealed, awaiting judgement'), (4, b'judged')]),
			preserve_default=True,
		),
		migrations.AddField(
			model_name='learner',
			name='study_hidden',
			field=models.ForeignKey(related_name='current_hidden_learners', default=None, blank=True, to='study.ActiveTranslation', help_text=b'The Translation that is the solution for study_shown (internal only).', null=True),
			preserve_default=True,
		),
		migrations.AddField(
			model_name='learner',
			name='study_shown',
			field=models.ForeignKey(related_name='current_shown_learners', default=None, blank=True, to='phrasebook.Translation', help_text=b'The Translation that is currently visible, if any (internal only).', null=True),
			preserve_default=True,
		),
		migrations.AddField(
			model_name='learner',
			name='study_answer',
			field=models.TextField(default=b'', help_text=b'The latest thing the user answered (internal only).'),
			preserve_default=True,
		),
	]
