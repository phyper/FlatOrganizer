from django.contrib.auth.models import User
from flats.models import UserProfile, Flat, Flat_Member, Category, Task, Assigned_Task, Invitation, UserProfile
import datetime

user1 = User.objects.create_user('gary', 'test@test.test', 'gary')
user1.first_name = 'Gary'
user1.last_name = 'Black'
user1.save()

user2 = User.objects.create_user('madonna', 'test@test.test', 'madonna')
user2.first_name = 'Madonna'
user2.last_name = 'Uknown'
user2.save()

profileM = UserProfile(user=user2)
profileM.save()

user3 = User.objects.create_user('rihanna', 'test@test.test', 'rihanna')
user3.first_name = 'Rihanna'
user3.last_name = 'Uknown'
user3.save()

flat1 = Flat(name='26 Winton Drive', description='----')
flat1.save()

flatmember1 = Flat_Member(user=user2, flat=flat1, join_date=datetime.datetime.now())
flatmember1.save()
flatmember2 = Flat_Member(user=user3, flat=flat1, join_date=datetime.datetime.now())
flatmember2.save()

flatmember5 = Flat_Member(user=user1, flat=flat1, join_date=datetime.datetime.now(), active=False)
flatmember5.save()

flat2 = Flat(name='28 Winton Drive', description='----')
flat2.save()

flatmember3 = Flat_Member(user=user1, flat=flat2, join_date=datetime.datetime.now())
flatmember3.save()

flat3 = Flat(name='30 Winton Drive', description='----')
flat3.save()

flat4 = Flat(name='Deleted fast Flat', description='----', active=False)
flat4.save()

flatmember5 = Flat_Member(user=user2, flat=flat4, join_date=datetime.datetime.now())
flatmember5.save()

flatmember4 = Flat_Member(user=user2, flat=flat3, join_date=datetime.datetime.now())
flatmember4.save()

cat1 = Category(name = "Cleaning")
cat1.save()

cat2 = Category(name = "Shopping")
cat2.save()

task1 = Task(name ="Clean the kitchen", description = "TestDesc", credits = 10, flat = flat1, category = cat1)
task1.save()
task2 = Task(name ="Toiletpaper", description = "TestPaper", credits = 5, flat = flat1, category = cat2)
task2.save()
task3 = Task(name ="Clean the shower", description = "TestShower", credits = 15, flat = flat1, category = cat1)
task3.save()
task4 = Task(name ="Vaccum cleaner bags", description = "Size 30x25", credits = 5, flat = flat1, category = cat2)
task4.save()

assigned1 = Assigned_Task(task = task1, member = flatmember1, creation_date = datetime.datetime.now(), completion_date = datetime.datetime.now())
assigned1.save()

invite1 = Invitation(flat=flat1, email = "invited@cool.com")
invite1.save()
