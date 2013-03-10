from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
import datetime
from PIL import Image
from django.forms import ModelForm

CATEGORY_CHOICES = (('Shopping', 'Shopping'),
                    ('Cleaning', 'Cleaning'),
                    ('Other','Other'),
    )

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

class Flat_Manager(models.Manager):
	def get_query_set(self):
		return super(Flat_Manager, self).get_query_set().filter(active=True)

class Flat(models.Model):
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=100)
	active = models.BooleanField(default=True, editable=False)
	objects = Flat_Manager()

	def __unicode__(self):
		return self.name
		
	def delete(self, *args, **kwargs):
		self.active = False
		self.save()
		members = Flat_Member.objects.filter(flat = self)
		for member in members:
			member.delete()

class Flat_Member_Manager(models.Manager):
	def get_query_set(self):
		return super(Flat_Member_Manager, self).get_query_set().filter(active=True)

class Flat_Member(models.Model):
	user = models.ForeignKey(User)
	flat = models.ForeignKey(Flat)
	join_date = models.DateTimeField(auto_now_add = True)
	active = models.BooleanField(default=True, editable=False)
	objects = Flat_Member_Manager()

	def __unicode__(self):
		return self.user.first_name + " " + self.flat.name

	def delete(self, *args, **kwargs):
		self.active = False
		self.save()

class Category(models.Model):
	name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

	def __unicode__(self):
		return self.name		

class Task(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=100)
	credits = models.IntegerField()
	flat = models.ForeignKey(Flat)
	category = models.ForeignKey(Category)

	def __unicode__(self):
		return self.name

class Assigned_Task(models.Model):
	task = models.ForeignKey(Task)
	member = models.ForeignKey(Flat_Member)
	creation_date = models.DateTimeField(auto_now_add = True)
	completion_date = models.DateTimeField(auto_now_add = True)

        def __unicode__(self):
            return self.member + " - " + self.task

class Invitation(models.Model):
        flat = models.ForeignKey(Flat)
        email = models.EmailField()

        def __unicode__(self):
            return  self.email

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
            'email' : forms.TextInput(attrs = {'placeholder': 'E-mail'}),
            }


class NewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "credits", "category"]

        widgets = {
            'name' : forms.TextInput(attrs = {'placeholder': 'Name'}),
            'description' : forms.TextInput(attrs = {'placeholder': 'Description'}),
            'credits' : forms.TextInput(attrs = {'placeholder': 'Credits'}),

            #'category' : forms.CharField(forms.Select(choices=CATEGORY_CHOICES)),
            }

class NewFlatForm(forms.ModelForm):
	class Meta:
		model = Flat
		fields = ["name", "description"]
		widgets = {
			'name' : forms.TextInput(attrs = {'placeholder': 'Name'}),
			'description' : forms.TextInput(attrs = {'placeholder': 'Description'}),
		}