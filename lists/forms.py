
from django.forms import ModelForm
from lists.models import TranslationsList, ListAccess
from study.models import ActiveTranslation


class ListForm(ModelForm):
	class Meta:
		model = TranslationsList
		fields = ('name', 'public', 'language',)


class ListAccessForm(ModelForm):
	class Meta:
		model = ListAccess
		fields = ('priority', 'active',)

	def save(self, *args, **kwargs):
		self.instance.learner.need_active_update = True
		self.instance.learner.need_active_update.save()


def update_translations_cache(access):
	# not used anymore
	# this was not the best way after all, can't update priority without checking all lists
	translations = access.translations_list.translations
	actives = ActiveTranslation.objects.filter(learner = access.learner, translation__in = translations.all())
	for active in actives:
		if access.active:
			active.active = True
		if access.priority > active.priority:
			active.priority = access.priority
		print 'saving', active
		active.save()


