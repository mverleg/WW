# -*- coding: utf-8 -*-

from django.db import models, migrations


class Migration(migrations.Migration):

	dependencies = [
		('study', '0007_result_verified'),
		('learners', '0008_min_delay_default'),
	]

	operations = [
		migrations.AddField(
			model_name='learner',
			name='study_answer',
			field=models.TextField(default=b'', help_text=b'The latest thing the user answered (internal only).'),
			preserve_default=True,
		),
		migrations.AddField(
			model_name='learner',
			name='study_hidden',
			field=models.ForeignKey(related_name='current_hidden_learners', default=None, blank=True, to='phrasebook.Translation', help_text=b'The Translation that is the solution for study_shown (internal only).', null=True),
			preserve_default=True,
		),
		migrations.AddField(
			model_name='learner',
			name='study_show_learn',
			field=models.BooleanField(default=True, help_text=b'Is the learning language phrase being shown, or asked for (so hidden) (internal only).'),
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
			name='study_state',
			field=models.PositiveSmallIntegerField(default=0, help_text=b'(internal only).', choices=[(0, b'nothing'), (1, b'asking meaning (showing learn lang)'), (3, b'revealed, awaiting judgement'), (4, b'judged')]),
			preserve_default=True,
		),
	]
