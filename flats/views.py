from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render_to_response
from flats.models import Flat, Flat_Member, UserProfile, Task, Assigned_Task, Invitation
from flats.forms import UserCreateForm, UserEditForm, UserProfileForm, NewFlatForm, NewTaskForm, EditFlatInfoForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import Http404
from django.core.exceptions import PermissionDenied
from tasklist.settings import MEDIA_ROOT
from django.core.mail import EmailMessage
from tasklist.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

# Index page

def index(request):
    context = RequestContext(request)
    success = None

    try:
        u = User.objects.get(username=request.user)
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
                #If email and password is set in the settings
                #then send an email
                if EMAIL_HOST_PASSWORD and EMAIL_HOST_USER:
                    send_email(email)
                success = True
            return HttpResponseRedirect("/flats")

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
                return HttpResponseRedirect("/flats")
            else:
                print (edit_flat_form.errors)

        return render_to_response('flats/index.html', { 'flats' : flats_user, 'flat_form' : new_flat_form, 'edit_form' : edit_flat_form, 'invited_flats' : invited_flats}, context)

    except:
        context = RequestContext(request)
        return render_to_response('flats/login.html', {}, context)


# User Registration
@login_required
def flat(request, flatid=None):
    context = RequestContext(request)
    u = User.objects.get(username=request.user)
    flat = Flat.objects.filter(id = flatid)
    full_list = Task.objects.filter(flat = flat)
    try:
        userFlatMember = Flat_Member.objects.get(user=u, flat=flat)
    except:
        #If user do not belong to flat
        raise PermissionDenied
    link = "/flats/" + flatid
    success = None
    user_lives_in_flat = livesInFlat(u, flat)

    if "deleteFlat" in request.POST and user_lives_in_flat:
        flat_id = request.POST.get('flat_id')
        flat = Flat.objects.get(id = flat_id)
        flat.delete()
        return HttpResponseRedirect("/flats")

    task_list = []
    shopping_list = []
    summaryList = []
    members_in_flat = Flat_Member.objects.filter(flat = flat)
    for member in members_in_flat:
        #Member
        row = []
        row.append(member.user.first_name)
        #Last task completed and date completed
        try:
            last_task = Assigned_Task.objects.filter(member = member).latest()
            last_task_name = last_task.task.name
            last_task_date = last_task.completion_date
        except:
            last_task_name = "N/A"
            last_task_date = "N/A"

        row.append(last_task_name)
        row.append(last_task_date)

        #total score
        total_score = 0
        for a_task in Assigned_Task.objects.filter(member = member):
            total_score = total_score + a_task.task.credits
        row.append(total_score)

        summaryList.append(row)

    for list_item in full_list:
        if list_item.category.name != "Shopping":
            task_list.append(list_item)
        else:
            shopping_list.append(list_item)

    flat_members = Flat_Member.objects.filter(flat=flat)

    new_task_form = NewTaskForm()

    if "setTaskDone" in request.POST and user_lives_in_flat:
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id = task_id)
        assigned_task = Assigned_Task()
        assigned_task.task = task
        assigned_task.member = userFlatMember
        assigned_task.save()
        return HttpResponseRedirect(link)

    if "setShoppingItemDone" in request.POST and user_lives_in_flat:
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id = task_id)
        assigned_task = Assigned_Task()
        assigned_task.task = task
        assigned_task.member = userFlatMember
        assigned_task.save()
        task.delete()

        full_list = Task.objects.filter(flat = flat )
        shopping_list = []

        for list_item in full_list:
            if list_item.category.name == "Shopping":
                shopping_list.append(list_item)
        return HttpResponseRedirect(link)

    if "deleteTaskItem" in request.POST and user_lives_in_flat:
        task_id = request.POST.get('task_id')
        print (task_id)
        task = Task.objects.get(id = task_id)
        task.delete()
        return HttpResponseRedirect(link)

    if "createNewItem" in request.POST and user_lives_in_flat:
        new_task_form = NewTaskForm(request.POST)

        if new_task_form.is_valid():
            task = new_task_form.save(commit=False)
            task.flat = flat[0]
            task.save()
            full_list = Task.objects.filter(flat = flat )
            task_list = []
            shopping_list = []

            for list_item in full_list:
                if list_item.category.name != "Shopping":
                    task_list.append(list_item)
                else:
                    shopping_list.append(list_item)
            
            return HttpResponseRedirect(link)
        else:
            print (new_task_form.errors)

    if user_lives_in_flat:
        return render_to_response('flats/flat.html', {'flat_info': flat[0], 'task_list' : task_list, 'shopping_list' : shopping_list, 'flat_members' : flat_members, 'task_form':new_task_form, 'summaryList':summaryList} , context)
    else:
        raise PermissionDenied


def register(request):
    context = RequestContext(request)
    success = False
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

            #Redirect user to the home page after successful registration
            try:
                user = auth.authenticate(username=uform['username'].value(), password=uform['password1'].value())
                auth.login(request, user)
                return HttpResponseRedirect("/flats/")
            except:
                raise Http404
        else:
            return render_to_response('flats/register.html', {'uform': uform, 'pform': pform}, context)
    else:
        uform = UserCreateForm()
        pform = UserProfileForm()
        return render_to_response('flats/register.html', {'uform': uform, 'pform': pform}, context)

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
            return render_to_response('flats/login.html', {'error':True}, context)
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
        try:
            view_user = User.objects.get(username=username)
            flat = Flat.objects.get(id=flatid)
        except:
            raise PermissionDenied
        #access is defined as both the user and the user to view lives in the
        #chosen flat
        access = livesTogetherWithUser(logged_in_user, view_user, flat)
        if access:
            view_member = Flat_Member.objects.get(user = view_user, flat=flat)
            tasks_assigned = Assigned_Task.objects.filter(member = view_member).order_by('-completion_date')

            sum_credits = 0
            for tasks in tasks_assigned:
                sum_credits = sum_credits + tasks.task.credits

            profile_picture = "/flats/imgs/standard.gif"
            try:
                if(view_user.get_profile() and view_user.get_profile().picture):
                    profile_picture = view_user.get_profile().picture.url
            except:
                print ("No user profile")
            return render_to_response('profiles/user_profile.html', {'member': view_member,
                                                                     'flat': flat,
                                                                     'tasks_assigned': tasks_assigned,
                                                                     'sum': sum_credits,
                                                                     'profile_picture': profile_picture },context)
        else:
            #Happens when user do not live in selected flat with the selected user
            raise PermissionDenied
    else:
        #if no user and flat is selected
        #you will be directed to own user profile
        #indepentend from flats
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

        profile_user = None
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

def livesInFlat(user, flat):
    flat_members = Flat_Member.objects.filter(flat = flat)
    for member in flat_members:
        if member.user == user:
            return True
    return False

def livesTogetherWithUser(logged_in_user, user_to_view, flat):
    return livesInFlat(logged_in_user, flat) and livesInFlat(user_to_view, flat)

def send_email(email_address):
    msg = EmailMessage('FlatOrganizer: Flat Invitation',
        'You got an invite! ' +
        'To accept this invitation, login or register for the FlatOrganizer with your email address ('+email_address+').'
        , to=[email_address])
    try:
        return msg.send()
    except:
        print ("Failed to send email to " + email_address)