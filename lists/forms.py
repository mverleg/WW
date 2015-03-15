
from django.forms import ModelForm
from lists.models import TranslationsList, ListAccess


class ListForm(ModelForm):
	class Meta:
		model = TranslationsList
		fields = ('name', 'language', 'public',)


class ListAccessForm(ModelForm):
	class Meta:
		model = ListAccess
		fields = ('priority', 'active',)

	def save(self, commit = True, *args, **kwargs):
		if hasattr(self.instance, 'learner'):
			self.instance.learner.need_active_update = True
			if commit:
				self.instance.learner.save()
		return super(ListAccessForm, self).save(commit, *args, **kwargs)


