
from django.contrib import admin
from study.models import Result, ActiveTranslation


class ActiveAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'translation', 'learner', 'score', 'priority', 'active',)


class ResultAdmin(admin.ModelAdmin):
	readonly_fields = ('when',)
	list_display = ('__str__', 'get_result_display', 'learner', 'asked', 'known', 'when',)


admin.site.register(ActiveTranslation, ActiveAdmin)
admin.site.register(Result, ResultAdmin)


