from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import get_user_model
from accounts.models import SalesProfile
from django.db import transaction

from django.core.files.images import get_image_dimensions

CHOICES = (('1', 'Admin',), ('2', 'Co-Admin',))

User = get_user_model()
class AdminForm(UserCreationForm):

	choice_field = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), choices=CHOICES, required=True)
	class Meta:
		model = User
		fields = ["username","email","password1","password2","full_name","image"]

		widgets = {
			'email'		: forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Email*'}),
			'username' 	: forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Username*'}),
			'password1' : forms.TextInput(attrs={'class': 'form-control' , 'placeholder':'Password*'}),
			'password2' : forms.TextInput(attrs={'class': 'form-control' , 'placeholder':'Password confirmation*'}),
			'full_name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Full Name'}),
		}


	@transaction.atomic
	def save(self,users):
		# *args, **kwargs

		user = super().save(commit=False)

		adminCheck = self.cleaned_data['choice_field']

		if adminCheck == '1' and users.is_admin and users.is_staff:
			user.is_admin = True
		elif adminCheck == '2':
			user.is_staff = True
		else:
			raise forms.ValidationError('You Have No Permission To Create Admin User. You Only Create Co-Admin')
		
		user.image = self.cleaned_data['image']
		user.save()
		return user
