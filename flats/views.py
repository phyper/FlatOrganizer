from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from flats.models import Flat, Flat_Member, UserProfile, UserCreateForm, UserEditForm, UserProfileForm, Task, Assigned_Task
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from crispy_forms.helper import FormHelper
from django.http import Http404
from django.core.exceptions import PermissionDenied

# Index page

def index(request):
	try: # This might need refactoring later as this is not the best way to check user's status
		u = User.objects.get(username=request.user)
		template = loader.get_template('flats/index.html')
		
		flats_user = Flat_Member.objects.filter(user=u)
	
		for fu in flats_user:
                    if fu.flat.active:
                        flat_members = Flat_Member.objects.filter(flat=fu.flat)
                        fu.member_list = flat_members
                    else:
                        fu.delete()
		
		context = RequestContext(request,{ 'flats' : flats_user})
		return HttpResponse(template.render(context))
	except:
		context = RequestContext(request)
		return render_to_response('flats/login.html', {}, context)

# User Registration view/Template

def flat(request, flatid=None):
    context = RequestContext(request)
    flat = Flat.objects.filter(id = flatid)
    full_list = Task.objects.filter(flat = flat )
    task_list = []
    shopping_list = []

    for list_item in full_list:
        if list_item.category.name != "Shopping":
            task_list.append(list_item)
        else:
            shopping_list.append(list_item)

    flat_members = Flat_Member.objects.filter(flat=flat)
    u = User.objects.get(username=request.user)
    access_right = False
    #One can access this if the logged in user
    #are member of the flat one wants to view
    for member in flat_members:
        if member.user == u:
            access_right = True
    if access_right:
        return render_to_response('flats/flat.html', {'flat_info': flat[0], 'task_list' : task_list, 'shopping_list' : shopping_list, 'flat_members' : flat_members} , context)
    else:
        raise PermissionDenied

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

@login_required
def profile(request, flatid=None, username=None):
    context = RequestContext(request)
    if flatid and username:
        logged_in_user = User.objects.get(username=request.user)
        logged_in_user_in_flat = False
        view_user_in_flat = False
        try:
            view_flat = Flat.objects.get(id=flatid)
            view_user = User.objects.get(username=username)
            flat_members_in_view_flat = Flat_Member.objects.filter(flat=view_flat)
            member_to_view = None
            for member in flat_members_in_view_flat:
                #One can only view persons in own flat
                if member.user == logged_in_user:
                    logged_in_user_in_flat = True
                #Person to look at need to belong to the selected flat
                if member.user == view_user:
                    view_user_in_flat = True
                    member_to_view = member
        except:
            #Happens when no valid flat number or username
            raise Http404
        if logged_in_user_in_flat and view_user_in_flat:
            tasks_assigned = Assigned_Task.objects.filter(member = member_to_view)
            #Sort the list later on by doing something like Assigned_Task.objects.order_by('')

            #Consider moved to another place
            sum_credits = 0
            for tasks in tasks_assigned:
                sum_credits = sum_credits + tasks.task.credits
            return render_to_response('profiles/user_profile.html', {'member': member_to_view,
                                                                     'flat': view_flat,
                                                                     'tasks_assigned': tasks_assigned,
                                                                     'sum': sum_credits}, context)
        else:
            #Happens when user do not live in selected flat
            raise PermissionDenied
    else:
        u_instance = request.user
        saved = ""
        if request.method == 'POST':
            u_form = UserEditForm(request.POST, instance=u_instance)
            p_form = UserProfileForm(request.POST)
            if u_form.is_valid():
                #p_form.save()
                u_form.save()
                saved = "Saved"
            else:
                print (u_form.errors)
                saved = "Error - not saved"
                #print p_form.errors
        else:
            u_form = UserEditForm(instance=u_instance)
            p_form = UserProfileForm()
        return render_to_response('profiles/edit_profile.html', {'uform': u_form, 'pform' : p_form, 'saved' : saved}, context)
