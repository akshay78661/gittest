from django.template import RequestContext
from django.contrib.auth.models import User
from blog.forms import UserForm, UserProfileForm
from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
	context = RequestContext(request)

	return render_to_response('blog/index.html', context)

def register(request):
	context = RequestContext(request)

	registered = False

	if request.method=='POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_active() and profile_form.is_active:
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()
			registered=True

		else:
			print(user_form.errors, profile_form.errors)

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render_to_response(
		'blog/register.html',
		{'user_form':user_form, 'profile_form':profile_form, 'registered':registered},
	context)					