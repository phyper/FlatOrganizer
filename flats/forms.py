from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from models import UserProfile, Task, Flat
from django.forms import CharField, PasswordInput

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required = True)
    password1 = CharField(widget=PasswordInput())
    password2 = CharField(widget=PasswordInput())

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1", "password2"]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['picture']

class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    email = forms.EmailField(required = True)
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
            }

class NewFlatForm(forms.ModelForm):
    class Meta:
        model = Flat
        fields = ["name", "description"]
        widgets = {
        'name' : forms.TextInput(attrs = {'placeholder': 'Name'}),
        'description' : forms.Textarea(attrs = {'placeholder': 'Description'}),
        }

class EditFlatInfoForm(forms.ModelForm):
    class Meta:
        model = Flat
        fields = ["name", "description"]
        widgets = {
        'name' : forms.TextInput(attrs = {'placeholder': 'Name'}),
        'description' : forms.Textarea(attrs = {'placeholder': 'Description'}),
        }