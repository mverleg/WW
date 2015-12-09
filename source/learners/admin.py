
from django.contrib import admin
from django.contrib.auth.models import Group
from learners.models import Learner


class LearnerAdmin(admin.ModelAdmin):
	exclude = ('groups',)
	fieldsets = (
		(None, {
			'fields': ('name', 'email', 'password',),
		}),
		('Permissions', {
			'fields': ('is_staff', 'is_superuser', 'user_permissions', 'last_login',),
		}),
		('Profile', {
			'fields': ('active_profile', 'profiles',),
		}),
		#('Settings', {
		#	'fields': ('ask_direction', 'favor_unknown', 'minimum_delay', 'new_count', 'show_medium_correctness',
		#		'show_correct_count', 'reward_magnitude',),
		#}),
		#('Internal only', {
		#	'fields': ('id', 'phrase_index', 'need_active_update', 'study_shown', 'study_hidden', 'study_state',
		#		'study_answer', 'study_active',),
		#	'classes': ('collapse',),
		#}),
	)
	readonly_fields = ('id', 'last_login', 'password',)
	list_display = ('name', 'email', 'is_staff', 'is_superuser',)


admin.site.register(Learner, LearnerAdmin)
admin.site.unregister(Group)


