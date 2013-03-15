from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = (('Shopping', 'Shopping'),
                    ('Cleaning', 'Cleaning'),
                    ('Other','Other'),
    )

class UserProfile (models.Model):
	user = models.OneToOneField(User)
	num_stars = models.IntegerField(default=0, editable=False)
	amount_of_points = models.IntegerField(default=0, editable=False)
	picture = models.ImageField(upload_to='imgs', blank=True)

class Flat_Manager(models.Manager):
	def get_query_set(self):
		return super(Flat_Manager, self).get_query_set().filter(active=True)

class Flat(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=200)
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
	
	def create_flat_member(self, user, flat):
	        flat_member = self.create(user=user, flat=flat)
	        return flat_member

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

class Task_Manager(models.Manager):
    def get_query_set(self):
        return super(Task_Manager, self).get_query_set().filter(active=True)

class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    credits = models.IntegerField()
    flat = models.ForeignKey(Flat)
    category = models.ForeignKey(Category)
    active = models.BooleanField(default=True, editable=False)
    objects = Task_Manager()

    def __unicode__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.active = False
        self.save()

class Assigned_Task(models.Model):
    task = models.ForeignKey(Task)
    member = models.ForeignKey(Flat_Member)
    creation_date = models.DateTimeField(auto_now_add = True)
    completion_date = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return self.member + " - " + self.task

    class Meta:
        get_latest_by = 'completion_date'

class Invitation(models.Model):
        flat = models.ForeignKey(Flat)
        email = models.EmailField()

        def __unicode__(self):
            return  self.email