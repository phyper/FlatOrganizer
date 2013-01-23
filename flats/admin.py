from flats.models import Person
from flats.models import Flat
from flats.models import Task
from django.contrib import admin

class PersonAdmin(admin.ModelAdmin):
	fieldsets = [
		('Personal information', {'fields': ['first_name', 'last_name']}),
		('Stars',                {'fields': ['num_stars']}),
	]
	
admin.site.register(Person, PersonAdmin)
admin.site.register(Flat)
admin.site.register(Task)
