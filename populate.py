from django.contrib.auth.models import User
from flats.models import UserProfile, Flat, Flat_Member, Category, Task, Assigned_Task, Invitation, UserProfile
import datetime

user1 = User.objects.create_user('gary', 'gary@black.com', 'gary')
user1.first_name = 'Gary'
user1.last_name = 'Black'
user1.save()

profile1 = UserProfile(user=user1)
profile1.picture = "Gary.jpg"
profile1.save()

user2 = User.objects.create_user('madonna', 'madonna@superstar.com', 'madonna')
user2.first_name = 'Madonna'
user2.last_name = 'Ciccone'
user2.save()

profile2 = UserProfile(user=user2)
profile2.picture = "Sally.png"
profile2.save()

user3 = User.objects.create_user('rihanna', 'rihanna@rihanna.us', 'rihanna')
user3.first_name = 'Rihanna'
user3.last_name = 'Fenty'
user3.save()

profile3 = UserProfile(user=user3)
profile3.save()

flat1 = Flat(name='26 Winton Drive', description='The ultimate home')
flat1.save()

flat2 = Flat(name='28 Winton Drive', description='A flat for the less lucky ones')
flat2.save()

flat3 = Flat(name='30 Winton Drive', description='Study flat')
flat3.save()

flat4 = Flat(name='Inactive flat', description='Long days, long nights', active=False)
flat4.save()


flatmember1 = Flat_Member(user=user2, flat=flat1, join_date=datetime.datetime.now())
flatmember1.save()

flatmember2 = Flat_Member(user=user3, flat=flat1, join_date=datetime.datetime.now())
flatmember2.save()

flatmember3 = Flat_Member(user=user1, flat=flat2, join_date=datetime.datetime.now())
flatmember3.save()

flatmember4 = Flat_Member(user=user2, flat=flat3, join_date=datetime.datetime.now())
flatmember4.save()

flatmember6 = Flat_Member(user=user3, flat=flat3, join_date=datetime.datetime.now())
flatmember6.save()

flatmember5 = Flat_Member(user=user1, flat=flat4, join_date=datetime.datetime.now(), active=False)
flatmember5.save()

cat1 = Category(name = "Chore")
cat1.save()

cat2 = Category(name = "Shopping")
cat2.save()

task1 = Task(name ="Clean the kitchen", description = "Remember own", credits = 10, flat = flat1, category = cat1)
task1.save()

task2 = Task(name ="Clean the shower", description = "Use the special soap", credits = 15, flat = flat1, category = cat1)
task2.save()

task3 = Task(name ="Take out garbage", description = "From kitchen and bathroom", credits = 4, flat = flat1, category = cat1)
task3.save()

task4 = Task(name ="Clean Toilet", description = "I know its bad..", credits = 25, flat = flat1, category = cat1)
task4.save()

task5 = Task(name ="Toiletpaper", description = "As Soon As Possible", credits = 5, flat = flat1, category = cat2, active=False)
task5.save()

task6 = Task(name ="Vaccum cleaner bags", description = "Size 30x25", credits = 5, flat = flat1, category = cat2)
task6.save()


task7 = Task(name ="Clean the kitchen", description = "Remember own", credits = 10, flat = flat2, category = cat1)
task7.save()

task8 = Task(name ="Clean the shower", description = "Use the special soap", credits = 15, flat = flat2, category = cat1)
task8.save()

task9 = Task(name ="Take out garbage", description = "From kitchen and bathroom", credits = 4, flat = flat3, category = cat1)
task9.save()

task10 = Task(name ="Clean Toilet", description = "I know its bad..", credits = 25, flat = flat3, category = cat1)
task10.save()

task11 = Task(name ="Toiletpaper", description = "As Soon As Possible", credits = 5, flat = flat3, category = cat2)
task11.save()

task12 = Task(name ="Vaccum cleaner bags", description = "Size 30x25", credits = 5, flat = flat4, category = cat2)
task12.save()

assigned1 = Assigned_Task(task = task1, member = flatmember1)
assigned1.save()

assigned2 = Assigned_Task(task = task2, member = flatmember1)
assigned2.save()

assigned4 = Assigned_Task(task = task5, member = flatmember1)
assigned4.save()

assigned5 = Assigned_Task(task = task7, member = flatmember3)
assigned5.save()

assigned6 = Assigned_Task(task = task8, member = flatmember3)
assigned6.save()

invite1 = Invitation(flat=flat1, email = "gary@black.com")
invite1.save()

invite2 = Invitation(flat=flat2, email = "madonna@superstar.com")
invite2.save()

invite3 = Invitation(flat=flat2, email = "rihanna@rihanna.us")
invite3.save()

invite4 = Invitation(flat=flat1, email = "demo@itech.com")
invite4.save()
