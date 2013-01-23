from django.db import models

# Create your models here.

class Person(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	num_stars = models.IntegerField()
	amount_of_points = models.IntegerField(); # can't edit this
	
	def __unicode__(self):
		return self.first_name
	
class Flat(models.Model):
	person = models.ForeignKey(Person) # each persn lives in a Flat (or several flats -> how to do)
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.name
	
class Task(models.Model):
	person = models.ForeignKey(Person) # each Task is related to a single Person
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=100)
	points = models.IntegerRangeField(min_value=1, max_value=10)
	
	def __unicode__(self):
		return self.name
		
	#points = models.IntegerField(choises=CHOISES, default=0)
	#CHOISES = (
	#	(0,0),(1,1),(2,2),(3,3),(4,4),(5,5)
	#)
