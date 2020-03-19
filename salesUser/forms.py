from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import get_user_model
from accounts.models import SalesProfile,districtBangladesh,bankListBangladesh
from django.db import transaction
from django.db.models import Count

from django.core.files.images import get_image_dimensions


# Get data
def get_my_district():
	return districtBangladesh.objects.values()


User = get_user_model()
class SalesRegistrationForm(UserCreationForm):
	# district		= forms.ModelChoiceField(required = True,queryset=districtBangladesh.objects.all(),widget=forms.Select(attrs={'class': 'form-control' , 'placeholder':'District'}))
	# company_name	= forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control' , 'placeholder':'Company Name'}))
	phone_number	= forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Phone Number'}))
	# payment_method	= forms.ModelChoiceField(required = False,queryset=bankListBangladesh.objects.all(),widget=forms.Select(attrs={'class': 'form-control' , 'placeholder':'Payment Method'}))
	# payment_account	= forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Payment Account'}))
	address = forms.CharField(required=False,widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Address'}))
	
	
	class Meta:
		model = User
		fields = ["username","email","password1","password2","full_name","image"]

		widgets = {
			'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Email*'}),
			'username' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Username*'}),
			'password1' : forms.TextInput(attrs={'class': 'form-control' , 'placeholder':'Password*'}),
			'password2' : forms.TextInput(attrs={'class': 'form-control' , 'placeholder':'Password confirmation*'}),
			'full_name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Full Name'}),

		}


	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		# user.first_name = self.cleaned_data['first_name']
		# user.last_name = self.cleaned_data['last_name']
		user.image = self.cleaned_data['image']
		user.is_general_user = True
		user.save()
		card = SalesProfile.objects.create(sales_user=user,company_address = self.cleaned_data.get('company_address'),
			phone_number=self.cleaned_data.get('phone_number'))
		# card.card_number.add(*self.cleaned_data.get('card_Number'))
		return user
