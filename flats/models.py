from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
import datetime
from PIL import Image
from django.forms import ModelForm



class UserProfile (models.Model):
	user = models.OneToOneField(User)
	num_stars = models.IntegerField(default=0, editable=False)
	amount_of_points = models.IntegerField(default=0, editable=False)
	picture = models.ImageField(upload_to='imgs', blank=True)
	
	#Accessing a users profile is done by calling user.get_profile(), 
	#but in order to use this function, Django needs to know where to 
	#look for the profile object.
	#So add this line to settings.py : AUTH_PROFILE_MODULE = "account.UserProfile"
	
	#def __unicode__(self):
	#   return self.user.username

#User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class Flat(models.Model):
	#persons = models.ManyToManyField(Person) # each person lives in a Flat (or several flats -> how to do)
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=100)
	#active = models.BooleanField() # a flat can be in use or not
	
	def __unicode__(self):
		return self.name

class Flat_Member(models.Model):
	user = models.ForeignKey(User)
	flat = models.ForeignKey(Flat)
	join_date = models.DateTimeField(auto_now_add = True)
	active = models.BooleanField() # a flat can be in use or not
	
	def __unicode__(self):
		return self.user.first_name + " " + self.flat.name 
			
class Category(models.Model):
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name		
	
class Task(models.Model):
	#person = models.ForeignKey(Person) # each Task is related to a single Person
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=100)
	credits = models.IntegerField() # try to limit value between 1 and 10
	flat = models.ForeignKey(Flat)
	category = models.ForeignKey(Category)
	#creation_date = models.DateTimeField(editable=False)
	#due_date = models.DateTimeField(editable=True)
	#completion_date = models.DateTimeField(editable=False)
	
	def __unicode__(self):
		return self.name
	
class Assigned_Task(models.Model):
	task = models.ForeignKey(Task)
	member = models.ForeignKey(Flat_Member)
	creation_date = models.DateTimeField(editable=False)
	completion_date = models.DateTimeField(editable=False)
	
class UserCreateForm(UserCreationForm):
	email = forms.EmailField(required = True)
	class Meta:
		model = User
		fields = ["first_name", "last_name", "email", "username"]

class UserProfileForm(forms.ModelForm):
	class Meta:	        
		model = UserProfile
		fields = ['picture']
		
class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ["first_name", "last_name", "email"]
                widgets = {
                    'first_name' : forms.TextInput(attrs = {'placeholder': 'First name'}),
                    'last_name' : forms.TextInput(attrs = {'placeholder': 'Last name'}),
                    'email'    : forms.TextInput(attrs = {'placeholder': 'E-mail'}),
                    }