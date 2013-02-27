from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from flats.models import Flat, Flat_Member, UserProfile, UserCreateForm, UserEditForm, UserProfileForm, Task
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from crispy_forms.helper import FormHelper

# Index page

def index(request):
	template = loader.get_template('flats/index.html')
	
	#flat_list = Flat_Member.objects.filter(user = request.user)
	u = User.objects.get(username=request.user)
	flats_user = Flat_Member.objects.filter(user=u)
	
	for fu in flats_user:
		flat_members = Flat_Member.objects.filter(flat=fu.flat)
		fu.member_list = flat_members
		print (fu.flat.name)
		print (fu.user)
		print (flat_members)
		
	#members = Flat_Member.objects.all()
	#members = Flat_Member.objects.get(user= request.user)
	context = RequestContext(request,{ 'flats' : flats_user})
	return HttpResponse(template.render(context))

# User Registration view/Template

def flat(request):
    context = RequestContext(request)

    flat = Flat.objects.filter(id = 1);
    full_list = Task.objects.filter(flat =flat )
    task_list = []
    shopping_list = []
    print (full_list)
    for list_item in full_list:
        print (list_item.category.name)

        if list_item.category.name != "Shopping":
            task_list.append(list_item)
        else:
            shopping_list.append(list_item)



    return render_to_response('flats/flat.html', {'flat_info': flat, 'task_list' : task_list, 'shopping_list' : shopping_list} , context)

def password_change(request):
    context = RequestContext(request)
    return render_to_response('flats/login.html', {}, context)

def resend_password(request):

	context = RequestContext(request)
	if request.method =='POST':
		passwdform = PasswordResetForm(data = request.POST)
		if passwdform.is_valid():
			passwdform.save()
			return render_to_response('flats/login.html', {}, context)
		
	return render_to_response('flats/resend_password.html', {}, context)

def register(request):
	context = RequestContext(request)
	registered = False
	if request.method =='POST':
		uform = UserCreateForm(data = request.POST)
		pform = UserProfileForm(data = request.POST)
		if uform.is_valid() and pform.is_valid():
			user = uform.save()
			profile = pform.save(commit = False)
			profile.user = user
			profile.save()
			registered = True
		else:
			print (uform.errors, pform.errors)
	else:
		uform = UserCreateForm()
		pform = UserProfileForm()
	return render_to_response('flats/register.html', {'uform': uform, 'pform': pform, 'registered': registered }, context)
	
def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
          username = request.POST.get('username', '')
          password = request.POST.get('password', '')
          user = auth.authenticate(username=username, password=password)
          if user is not None:
              if user.is_active:
                  auth.login(request, user)
                  # Redirect to index page.
                  return HttpResponseRedirect("/flats/")
              else:
                  # Return a 'disabled account' error message
                  return HttpResponse("You're account is disabled.")
          else:
              # Return an 'invalid login' error message.
              print  ("invalid login details " + username + " " + password)
              return render_to_response('flats/login.html', {}, context)
    else:
        # the login is a  GET request, so just show the user the login form.
        return render_to_response('flats/login.html', {}, context)

@login_required
def user_logout(request):
    context = RequestContext(request)
    logout(request)
    # Redirect back to index page.
    return HttpResponseRedirect('//')

## Not sure about this
#@login_required
#def view_profile(request):
#	user_profile = request.user.get_profile()

@login_required
def profile(request):
    context = RequestContext(request)
    u_instance = request.user
    if request.method == 'POST':
        u_form = UserEditForm(request.POST, instance=u_instance)
        p_form = UserProfileForm(request.POST)
        if u_form.is_valid():
            #p_form.save()
            u_form.save()
        else:
            print (u_form.errors)
            #print p_form.errors
    else:
        u_form = UserEditForm(instance=u_instance)
        p_form = UserProfileForm()

    return render_to_response('profiles/edit_profile.html', {'uform': u_form, 'pform' : p_form}, context)
