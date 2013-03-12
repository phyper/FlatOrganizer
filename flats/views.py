from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from flats.models import Flat, Flat_Member, UserProfile, UserCreateForm, UserEditForm, UserProfileForm, NewFlatForm, NewTaskForm, EditFlatInfoForm, Task, Assigned_Task, Invitation
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from crispy_forms.helper import FormHelper
from django.http import Http404
from django.core.exceptions import PermissionDenied, ValidationError
from tasklist.settings import MEDIA_ROOT
from django.core.files import File

# Index page

def index(request):
    context = RequestContext(request)
    success = None

    try: # This might need refactoring later as this is not the best way to check user's status
        u = User.objects.get(username=request.user)
        template = loader.get_template('flats/index.html')
        flats_user = Flat_Member.objects.filter(user=u)

        for fu in flats_user:
            flat_members = Flat_Member.objects.filter(flat=fu.flat)
            fu.member_list = flat_members

            if fu.flat.active:
                flat_members = Flat_Member.objects.filter(flat=fu.flat)
                fu.member_list = flat_members
            else:
                fu.delete()

        #Get all flats to check if on invite lists
        invited_flats = []
        flats = Flat.objects.all()
        for flat in flats:
            invites = Invitation.objects.filter(flat = flat)
            for invite in invites:
                if invite.email == u.email:
                    invited_flats.append(flat)

        # Create a new flat form
        new_flat_form = NewFlatForm()

        # Accept a new invite to join a flat
        if "acceptInvite" in request.POST :
            flat_id = request.POST.get('flat_id')
            flat = Flat.objects.get(id = flat_id)
            already_member = False
            for m in Flat_Member.objects.filter(flat = flat):
                if m.user == u:
                    already_member = True
            if not already_member:
                member = Flat_Member.objects.create_flat_member(u, flat)
                member.save()
                success = True

            invites = Invitation.objects.filter(flat = flat)
            for invite in invites:
                if invite.email == u.email:
                    invite.delete()
                    invited_flats.remove(flat)
            return HttpResponseRedirect("/flats")

        # Ask people to join your flat
        if "sendInvite" in request.POST :
            flat_id = request.POST.get('flat_id')
            email = request.POST.get('email')
            flat = Flat.objects.get(id = flat_id)
            already_member = False
            already_invited = False
            members = Flat_Member.objects.filter(flat = flat)
            for member in members:
                if member.user.email == email:
                    already_member = True
            invites = Invitation.objects.filter(flat = flat)
            for invite in invites:
                if invite.email == email:
                    already_invited = True

            if not already_member and not already_invited:
                newInvite = Invitation()
                newInvite.flat = flat
                newInvite.email = email
                newInvite.save()
                success = True

        # Create a new flat
        if "createNewFlat" in request.POST:
            new_flat_form = NewFlatForm(request.POST)
            if new_flat_form.is_valid():
                flat = new_flat_form.save(commit=False)
                flat.save()
                success = True

                # Link a created flat to current user
                flat_member = Flat_Member.objects.create_flat_member(u, flat)
                flat_member.save()
                return HttpResponseRedirect("/flats")
            else:
                print (new_flat_form.errors)

        # Remove a flat
        
        if "deleteFlat" in request.POST :
            flat_member_id = request.POST.get('flat_id')
            print(flat_member_id)
            flat_member = Flat_Member.objects.get(id=flat_member_id)
            flat_member.delete()
            return HttpResponseRedirect("/flats")

        edit_flat_form = EditFlatInfoForm()

        if "editFlatInfo" in request.POST:
            edit_flat_form = EditFlatInfoForm(request.POST)
            if edit_flat_form.is_valid():	
                flat_id = request.POST.get('flat_flat_id')
                flat = Flat.objects.get(id = flat_id)
                name = edit_flat_form.cleaned_data['name']
                description = edit_flat_form.cleaned_data['description']
                flat.name = name
                flat.description = description
                flat.save()
                success = True
                return HttpResponseRedirect("/flats")
            else:
                print (edit_flat_form.errors)

        response = render_to_response('flats/index.html', { 'flats' : flats_user, 'flat_form' : new_flat_form, 'edit_form' : edit_flat_form, 'invited_flats' : invited_flats, 'success': success}, context)
        return response

    except:
        context = RequestContext(request)
        return render_to_response('flats/login.html', {}, context)

# User Registration view/Template
@login_required
def flat(request, flatid=None):
    context = RequestContext(request)
    u = User.objects.get(username=request.user)

    if "deleteFlat" in request.POST:
        flat_id = request.POST.get('flat_id')
        flat = Flat.objects.get(id = flat_id)
        flat.delete()
        return render_to_response('flats/index.html', {}, context)

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

    access_right = False
    #One can access this if the logged in user
    #are member of the flat one wants to view
    userFlatMember = u
    for member in flat_members:
        if member.user == u:
            access_right = True
            userFlatMember = member

    new_task_form = NewTaskForm()
    if access_right:
        response =  render_to_response('flats/flat.html', {'flat_info': flat[0], 'task_list' : task_list, 'shopping_list' : shopping_list, 'flat_members' : flat_members, 'task_form':new_task_form} , context)
    else:
        raise PermissionDenied

    #Do one common processing here..
    if "setTaskDone" in request.POST:
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id = task_id)
        assigned_task = Assigned_Task()
        assigned_task.task = task
        assigned_task.member = userFlatMember
        assigned_task.save()
        success = True
        response =  render_to_response('flats/flat.html', {'flat_info': flat[0], 'task_list' : task_list, 'shopping_list' : shopping_list, 'flat_members' : flat_members, 'task_form':new_task_form, 'success': success} , context)

    if "setShoppingItemDone" in request.POST:
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id = task_id)
        assigned_task = Assigned_Task()
        assigned_task.task = task
        assigned_task.member = userFlatMember
        assigned_task.save()
        success = True
        task.delete()

        #Need to get the new list. This is ugly and needs refactoring
        full_list = Task.objects.filter(flat = flat )
        shopping_list = []

        for list_item in full_list:
            if list_item.category.name == "Shopping":
                shopping_list.append(list_item)
        response =  render_to_response('flats/flat.html', {'flat_info': flat[0], 'task_list' : task_list, 'shopping_list' : shopping_list, 'flat_members' : flat_members, 'task_form':new_task_form, 'success' : success} , context)





    if request.method == 'POST':
        new_task_form = NewTaskForm(request.POST)

        if new_task_form.is_valid():
            #new_task_form.fields['Flat'] = flat
            task = new_task_form.save(commit=False)
            task.flat = flat[0]
            task.save()
            success = True

            #Ugly as shit, but works for now
            full_list = Task.objects.filter(flat = flat )
            task_list = []
            shopping_list = []

            for list_item in full_list:
                if list_item.category.name != "Shopping":
                    task_list.append(list_item)
                else:
                    shopping_list.append(list_item)

            response =  render_to_response('flats/flat.html', {'flat_info': flat[0], 'task_list' : task_list, 'shopping_list' : shopping_list, 'flat_members' : flat_members, 'task_form':new_task_form, 'success' : success} , context)
        else:
            print (new_task_form.errors)


    return response

def update_task_in_flat_model(response):
    print (response)


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
            user.save()
            profile = pform.save(commit = False)
            profile.user = user
            
            # If the user has selected profile picture, select it, otherwise use standard picture
            if request.FILES:
                picture = save_file(request.FILES['picture'])
                profile.picture = picture
            else:
                profile.picture = "standard.gif"
            profile.save()
            registered = True
            
            # Redirect user to the home page after succesfull registration
            try:
                user = auth.authenticate(username=uform['username'].value(), password=uform['password1'].value())
                auth.login(request, user)
                return HttpResponseRedirect("/flats/")
            except:
                raise Http404
        else:
            return render_to_response('flats/register.html', {'uform': uform, 'pform': pform, 'registered': registered }, context)
    else:
        uform = UserCreateForm()
        pform = UserProfileForm()
        return render_to_response('flats/register.html', {'uform': uform, 'pform': pform, 'registered': registered }, context)

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                # Redirect to index page.
                return HttpResponseRedirect("/flats/")
            else:
                # Return a 'disabled account' error message
                return HttpResponse("Your account is disabled.")
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
        profile_user = None
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

            profile_picture = "/flats/imgs/standard.gif"
            try:
                if(view_user.get_profile() and view_user.get_profile().picture):
                    profile_picture = view_user.get_profile().picture.url
            except:
                print ("No user profile")
            return render_to_response('profiles/user_profile.html', {'member': member_to_view,
                                                                     'flat': view_flat,
                                                                     'tasks_assigned': tasks_assigned,
                                                                     'sum': sum_credits,
                                                                     'profile_picture': profile_picture },context)
        else:
            #Happens when user do not live in selected flat
            raise PermissionDenied
    else:
        user = request.user
        saved = ""
        if request.method == 'POST':
            u_form = UserEditForm(request.POST, instance=user)
            if u_form.is_valid():
                u_form.save()
                saved = "Saved"
            else:
                print (u_form.errors)
                saved = "Error - not saved"
        else:
            u_form = UserEditForm(instance=user)


        profile_picture = "/flats/imgs/standard.gif"
        try:
            profile_user = UserProfile.objects.get(user=user)
            if(profile_user and profile_user.picture):
                profile_picture = profile_user.picture.url
        except:
            print ("No user profile")
        return render_to_response('profiles/edit_profile.html', {'uform': u_form, 'saved' : saved, 'profile_picture' : profile_picture}, context)



def save_file(file, path=''):
    filename = file._get_name()
    fd = open('%s/%s' % (MEDIA_ROOT, str(path) + str(filename)), 'wb' )
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()
    return filename
