from django import forms
from django.db import transaction
from product_showcase.models import Product_Type,Product_Speciality,Product_list


class Product_Showcase_form(forms.Form):


	name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Product Name'}),required=True)
	details = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Product Details'}),required=True)
	product_type = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),queryset=Product_Type.objects.all())
	
	product_speciality = forms.ModelMultipleChoiceField(
        queryset=Product_Speciality.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True
    )

	class Meta:
		model = Product_list
		# fields = ["name","details"]
		# widgets = {
		# 	'name'		: forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Email*'}),
		# 	'details' 	: forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Username*'}),
			
		# }
		
			
	
		