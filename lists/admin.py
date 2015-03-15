
from django.contrib import admin
from lists.models import TranslationsList, ListAccess


class ListAccessAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'translations_list', 'learner', 'active', 'access', 'priority',)

	def save(self, *args, **kwargs):
		self.instance.learner.need_active_update = True
		self.instance.learner.save()
		super(ListAccessAdmin, self).save(*args, **kwargs)


class TranslationListAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'language',)


admin.site.register(TranslationsList, TranslationListAdmin)
admin.site.register(ListAccess, ListAccessAdmin)


