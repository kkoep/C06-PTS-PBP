from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User

class UserAuthenticationForm(forms.Form):
    email = forms.CharField(label="email", min_length=1, max_length=50)
    password = forms.CharField(label="password", widget=forms.PasswordInput)
        

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

	class Meta:
		model = User
		fields = ('email', 'username', 'password1', 'password2', 'nama', 'role')

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = User.objects.exclude(pk=self.instance.pk).get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % email)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			user = User.objects.exclude(pk=self.instance.pk).get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)

