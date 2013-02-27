from django.contrib.auth.models import User
from flats.models import UserProfile, Flat, Flat_Member, Category, Task, Assigned_Task
import datetime

user1 = User.objects.create_user('gary', 'test@test.test', 'gary')
user1.first_name = 'Gary'
user1.last_name = 'Black'
user1.save()

user2 = User.objects.create_user('madonna', 'test@test.test', 'madonna')
user2.first_name = 'Madonna'
user2.last_name = 'Uknown'
user2.save()

user3 = User.objects.create_user('rihanna', 'test@test.test', 'rihanna')
user3.first_name = 'Rihanna'
user3.last_name = 'Uknown'
user3.save()

flat1 = Flat(name='26 Winton Drive', description='----')
flat1.save()

Flat_Member(user=user1, flat=flat1, join_date=datetime.datetime.now(), active=True).save()
Flat_Member(user=user2, flat=flat1, join_date=datetime.datetime.now(), active=True).save()
Flat_Member(user=user3, flat=flat1, join_date=datetime.datetime.now(), active=True).save()

flat2 = Flat(name='28 Winton Drive', description='----')
flat2.save()

Flat_Member(user=user1, flat=flat2, join_date=datetime.datetime.now(), active=False).save()

flat3 = Flat(name='30 Winton Drive', description='----')
flat3.save()

Flat_Member(user=user2, flat=flat3, join_date=datetime.datetime.now(), active=False).save()

