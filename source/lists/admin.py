
from django.contrib import admin
from lists.models import TranslationsList, ListAccess


class ListAccessAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'translations_list', 'learner', 'active', 'access', 'priority',)

	def save(self, *args, **kwargs):
		self.instance.learner.need_update()
		super(ListAccessAdmin, self).save(*args, **kwargs)


class TranslationListAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'language',)

	def save(self, *args, **kwargs):
		for need_update_access in ListAccess.objects.filter(translations_list = li):
			need_update_access.learner.need_update()
		super(TranslationListAdmin, self).save(*args, **kwargs)


admin.site.register(TranslationsList, TranslationListAdmin)
admin.site.register(ListAccess, ListAccessAdmin)


