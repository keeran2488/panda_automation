import os
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.views.generic import CreateView
from django.contrib.auth.forms import (UserCreationForm,PasswordChangeForm)
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


from product_showcase.models import Product_Type,Product_Speciality,Product_list
from product_showcase.forms import Product_Showcase_form


def prodect_type(request):
	if request.method == 'POST':
		product_type_nameOne 	= request.POST['product_type_name1']
		product_type_nameTwo 	= request.POST['product_type_name2']

		info = Product_Type.objects.filter(id=1).update(product_type_name=product_type_nameOne)
		infoTwo = Product_Type.objects.filter(id=2).update(product_type_name=product_type_nameTwo)

		if info and infoTwo:

			data = Product_Type.objects.filter(id=1)
			data2 = Product_Type.objects.filter(id=2)

			context = {'panda':data,'panda2':data2,'success':'Update Offers Type',"navActive":"ProductShowcase"}
			return render(request,"productShowcase/product_type.html",context)
		else:
			data = Product_Type.objects.filter(id=1)
			data2 = Product_Type.objects.filter(id=2)

			context = {'panda':data,'panda2':data2,'error':'Update Error',"navActive":"ProductShowcase"}
			return render(request,"productShowcase/product_type.html",context)

	data = Product_Type.objects.filter(id=1)
	data2 = Product_Type.objects.filter(id=2)
	context = {"panda":data, "panda2":data2,"navActive":"ProductShowcase"}
	return render(request,"productShowcase/product_type.html",context)


def productSpeciality(request):

	if request.method == 'POST':
		product_speciality = request.POST['product_speciality_name']
		product_speciality_details = request.POST['product_speciality_details']

		try:
			info =  Product_Speciality.objects.create(product_speciality_name=product_speciality,product_speciality_details=product_speciality_details)

			if info:
				product_speciality=""
				product_speciality_details=""
				data = Product_Speciality.objects.all()
				context = {"panda":data,"success":"Save Successfully","navActive":"ProductShowcase"}
				return render(request,"productShowcase/product_speciality.html",context)
			else:
				data = Product_Speciality.objects.all()
				context = {"panda":data,"error":"Error to Save","navActive":"ProductShowcase"}
				return render(request,"productShowcase/product_speciality.html",context)
		except Exception as e:
			data = Product_Speciality.objects.all()
			context = {"panda":data,"error":e,"navActive":"ProductShowcase"}
			return render(request,"productShowcase/product_speciality.html",context)



	data = Product_Speciality.objects.all()
	context = {"panda":data,"navActive":"ProductShowcase"}
	return render(request,"productShowcase/product_speciality.html",context)


def productSpecialityDelete(request):
	if request.user.is_admin:
		data = Product_Speciality.objects.all()
		data.delete()
	return redirect('productSpeciality')

def productSpecialityDeleteByID(request,id):
	if request.user.is_admin:
		data = Product_Speciality.objects.filter(id=id)
		data.delete()
	return redirect('productSpeciality')


def productShowcase(request):
	if request.method == 'POST':
		form = Product_Showcase_form(request.POST)
		try:
			if form.is_valid():
				name               = form.cleaned_data["name"]
				details            = form.cleaned_data["details"]
				product_type       = form.cleaned_data["product_type"]
				product_speciality = form.cleaned_data.get('product_speciality')

				info = Product_list.objects.create(name=name,details=details,product_type=product_type)
				for product_speciality in product_speciality:
					info.product_speciality.add(product_speciality)

				if info:
					form = Product_Showcase_form()
					context = {"form":form,"success":"Save Successfully","navActive":"ProductShowcase"}
					return render(request,"productShowcase/product_showCase.html",context)
				else:
					form = Product_Showcase_form()
					context = {"form":form,"error":"Data Not Save","navActive":"ProductShowcase"}
					return render(request,"productShowcase/product_showCase.html",context)
			else:
				form = Product_Showcase_form()
				context = {"form":form,"error":"Data Not Save","navActive":"ProductShowcase"}
				return render(request,"productShowcase/product_showCase.html",context)


		except Exception as e:
			form = Product_Showcase_form()
			context = {"form":form,"error":e,"navActive":"ProductShowcase"}
			return render(request,"productShowcase/product_showCase.html",context)
			
	form = Product_Showcase_form()
	context = {"form":form,"navActive":"ProductShowcase"}
	return render(request,"productShowcase/product_showCase.html",context)
	

def product_list_show(request):
	info = Product_list.objects.all()
	context = {"panda":info,"navActive":"ProductShowcase"}
	return render(request,"productShowcase/product_list.html",context)

def product_listDeleteAll(request):
	if request.user.is_admin:
		info = Product_list.objects.all()
		info.delete()
	return redirect("product_list_show")

def product_listDeleteByID(request,id):
	if request.user.is_admin:
		info = Product_list.objects.filter(id=id)
		info.delete()
	return redirect("product_list_show")