from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
import json
from .forms import RegistrationForm, UserAuthenticationForm

#@login_required(login_url='/login/login_page/')
def landing_page(request):
    context = {
		'user': request.user.username,
	}
    return render(request, 'landing.html')

def login_page(request):
	context = {}
	# user = request.user
	# if user.is_authenticated:
	# 	return redirect('daftar_project:index_daftar_project')

	if request.POST:
		form = UserAuthenticationForm(request.POST)
		print(form.errors)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)
			print(user)
			if user:
				login(request, user)
				return redirect('/')
				
	else:
		form = UserAuthenticationForm()
	context['login_form'] = form

	return render(request, "login.html", context)

def signup(request):
	user = request.user
	if user.is_authenticated: 
		return HttpResponse("<h3>Anda sudah masuk ke akun dengan email " + str(user.email) + "</h3>")

	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		data = {}
		if form.is_valid():
			o = form.save()
			print(o.role)
			data['success'] = True
			return redirect('login:landing_page')
		else:
			data['error'] = form.errors
			data['success'] = False
			context['registration_form'] = form
			return HttpResponse(json.dumps(data), content_type='application/json')

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'signup.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('login:landing_page'))
    return response