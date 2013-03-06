from flats.models import UserProfile
from flats.models import Flat
from flats.models import Task
from flats.models import Flat_Member
from flats.models import Assigned_Task
from django.contrib import admin

class PersonAdmin(admin.ModelAdmin):
	fieldsets = [
		('Personal information', {'fields': ['first_name', 'last_name']}),
		('Stars',                {'fields': ['num_stars']}),
	]
	
admin.site.register(UserProfile)
admin.site.register(Flat)
admin.site.register(Task)
admin.site.register(Flat_Member)
admin.site.register(Assigned_Task)
