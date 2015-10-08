
from django.contrib import admin
from study.models import Result, ActiveTranslation


class ScoreDBAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'learner')


class ActiveAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'translation', 'scoredb', 'score', 'priority', 'active',)


class ResultAdmin(admin.ModelAdmin):
	readonly_fields = ('when',)
	list_display = ('__str__', 'get_result_display', 'scoredb', 'asked', 'known', 'when',)


admin.site.register(ActiveTranslation, ActiveAdmin)
admin.site.register(Result, ResultAdmin)


