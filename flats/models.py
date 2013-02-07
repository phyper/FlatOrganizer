from django.db import models
from django.contrib.auth.models import User
import datetime
from PIL import Image

class UserProfile (models.Model):
	user = models.OneToOneField(User)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField()
	num_stars = models.IntegerField()
	amount_of_points = models.IntegerField(editable=False)
 	avatar = models.ImageField(upload_to='images')
	
	#def __unicode__(self):
     #   return self.user.username

class Person(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField()
	num_stars = models.IntegerField()
	amount_of_points = models.IntegerField(editable=False) # can't edit this
	
	def __unicode__(self):
		return self.first_name
	
class Flat(models.Model):
	persons = models.ManyToManyField(Person) # each person lives in a Flat (or several flats -> how to do)
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=100)
	active = models.BooleanField() # a flat can be in use or not
	
	def __unicode__(self):
		return self.name
	
class Task(models.Model):
	#person = models.ForeignKey(Person) # each Task is related to a single Person
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=100)
	credits = models.IntegerField() # try to limit value between 1 and 10
	#category = models.OneToOneField(Category)
	#creation_date = models.DateTimeField(editable=False)
	#due_date = models.DateTimeField(editable=True)
	#completion_date = models.DateTimeField(editable=False)
	
	def __unicode__(self):
		return self.name
	
#class Assigned_Task(models.Model):
#	task = models.OneToOneField(Person)
#	person = models.OneToOneField(Person)
#	flat = models.OneToOneField(Person)
#	creation_date = models.DateTimeField(editable=False)
#	due_date = models.DateTimeField(editable=True)
#	completion_date = models.DateTimeField(editable=False)
	
class Category(models.Model):
	name = models.CharField(max_length=100)
		
	def __unicode__(self):
		return self.name