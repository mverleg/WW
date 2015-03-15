
from django.contrib import admin
from study.models import Result


class ResultAdmin(admin.ModelAdmin):
	readonly_fields = ('when',)
	list_display = ('get_result_display', 'learner', 'asked', 'known', 'when',)


admin.site.register(Result, ResultAdmin)


