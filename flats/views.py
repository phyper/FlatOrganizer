from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from flats.models import UserProfile
from flats.models import UserForm, UserProfileForm

# Index page

def index(request):
	template = loader.get_template('flats/index.html')
	context = RequestContext(request,{})
	return HttpResponse(template.render(context))

# User Registration view/Template

def register(request):
	context = RequestContext(request)
	registered = False
	if request.method =='Post':
		uform = UserForm(data = request.POST)
		pform = UserProfileForm(data = request.POST)
		if uform.is_valid() and pform.is_valid():
			user = uform.save()
			profile = pform.save(commit = False)
			profile.user = user
			profile.save()
			registered = True
		else:
			print uform.errors, pform.errors
	else:
		uform = UserForm()
		pform = UserProfileForm()
	return render_to_response('flats/register.html', {'uform': uform, 'pform': pform, 'registered': registered }, context)
	

## Not sure about this
#@login_required
#def view_profile(request):
#	user_profile = request.user.get_profile()
	
