import os
from django.conf import settings
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from accounts.models import (MyUser,MyDevice,Message_Notification,SalesProfile,
	Message_Notification_Read,Message_Notification,districtBangladesh,bankListBangladesh)
from django.core import serializers

from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models import Q

from administrationSection.forms import AdminForm

from django.contrib.auth.decorators import login_required

from fcm.utils import get_device_model

from django.template.loader import render_to_string

import json
import pandas as pd
import xlwt

@login_required(login_url='login_view')
def createAdmin(request):
	if request.user.is_admin:
		if request.method == 'POST':
			form = AdminForm(request.POST,request.FILES)
			try:
				if form.is_valid():
					form.image = form.cleaned_data["image"]
					adminCheck = form.cleaned_data["choice_field"]
					if adminCheck == 1:
						form.is_admin = True
					else:
						form.is_staff = True
					form.save(request.user)
					form = AdminForm()
					context = 	{'form':form,'success': 'Saved Data','navActive':'administration'}
					return render(request,'administration/createAdmin.html',context)
				else:
					context = 	{'form':form,'navActive':'administration'}
					return render(request,'administration/createAdmin.html',context)

			except Exception as e:
				form = AdminForm()
				context = {'errorCreate':e,'form':form,'navActive':'administration'}
				return render(request,'administration/createAdmin.html',context)

		form = AdminForm()
		context = {'form':form,'navActive':'administration'}
		return render(request,'administration/createAdmin.html',context)
	else:
		context = {'error':'You have no permission to make user','navActive':'administration'}
		return render(request,'administration/createAdmin.html',context)

@login_required(login_url='login_view')
def listAdmin(request):
	pand = User.objects.filter(Q(is_staff=True) | Q(is_admin=True))
	context = {'panda':pand,'navActive':'administration'}
	return render(request,'administration/listAdmin.html',context)

# Delete Section
@login_required(login_url='login_view')
def deleteAdminAll(request):
	if request.user.is_admin and request.user.is_staff == False:
		data = User.objects.filter(~Q(Q(is_admin=True) &Q(is_staff=True) & Q(is_general_user=True)) & ~Q(is_general_user=True) & ~Q(username=request.user.username) & ~Q(is_admin=True))
		data.delete()
		return redirect('listAdmin')

	if request.user.is_admin and request.user.is_staff and request.user.is_general_user:
		data = User.objects.filter(~Q(username=request.user.username) & ~Q(Q(is_general_user=True) & Q(is_admin=False) & Q(is_staff=False)))
		data.delete()
		return redirect('listAdmin')

@login_required(login_url='login_view')
def delete_Admin(request,id):
	if request.user.is_admin and request.user.is_staff == False:
		data = MyUser.objects.filter(Q(pk=id) & ~Q(username=request.user.username) & ~Q(is_admin=True))
		data.delete()
		return redirect('listAdmin')

	if request.user.is_admin and request.user.is_staff and request.user.is_general_user:
		data = MyUser.objects.filter(Q(pk=id) & ~Q(username=request.user.username))
		data.delete()
		return redirect('listAdmin')
	return redirect('listAdmin')

# User data Export
@login_required(login_url='login_view')
def export_users_xl_UserAdmin(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="Admin User.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Users')

	# Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Name','Username','E-mail','Image']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	# Sheet body, remaining rows
	font_style = xlwt.XFStyle()

	rows = MyUser.objects.filter(~Q(Q(is_general_user=True) & Q(is_admin=False) & Q(is_staff=False))).values_list('full_name',
		'username','email','image')

	for row in rows:
		row_num += 1
		for col_num in range(len(row)):
			# print(row[col_num])
			ws.write(row_num, col_num, str(row[col_num]), font_style)

	wb.save(response)
	return response

@login_required(login_url='login_view')
def messaging(request):

	my_phone = MyDevice.objects.all()

	if request.method == 'POST':
		# Device = get_device_model()
		message 		= request.POST['message']
		title 			= request.POST['titel']
		userSelect 		= request.POST.getlist('userSelect')
		DistrictSelect 	= request.POST.getlist('districtSelect')

		data = {}
		data['message'] = message
		data['title'] = title
		json_data = json.dumps(data)

		mez = Message_Notification.objects.create(title=title,message=message)
		mez.save()

		if DistrictSelect:

			for DistrictSelect in DistrictSelect:
				data2 = SalesProfile.objects.filter(district_name = DistrictSelect)
				for data2 in data2:
					my_phone = MyDevice.objects.filter(Q(user=data2.sales_user.id) & Q(is_active=True))
					userMy = MyUser.objects.only('id').get(id=data2.sales_user.id)
					readMez = Message_Notification_Read.objects.create(user_Message=userMy,message=mez)
					readMez.save()
					my_phone.send_message({'messages': json_data}, collapse_key='something')
					print(my_phone)

			my_phone = MyDevice.objects.all()
			district = districtBangladesh.objects.all()
			context 	= 	{'panda':my_phone,'success': 'Send Message Successfully','district':district,'navActive':'notification'}
			return render(request,'administration/notification.html',context)

		else:
			# print(json_data)
			if userSelect:
				for userID in userSelect:
					my_phone = MyDevice.objects.filter(Q(user=userID) & Q(is_active=True))
					userMy = MyUser.objects.only('id').get(id=userID)
					readMez = Message_Notification_Read.objects.create(user_Message=userMy,message=mez)
					readMez.save()	
					my_phone.send_message({'messages': json_data}, collapse_key='something')
			else:
				my_phone = MyDevice.objects.filter(is_active=True)
				for my_phone in my_phone:
					userMy = MyUser.objects.only('id').get(id=my_phone.user.id)
					readMez = Message_Notification_Read.objects.create(user_Message=userMy,message=mez)
					readMez.save()
				MyDevice.objects.filter(is_active=True).send_message({'messages': json_data}, collapse_key='something')
					

			my_phone = MyDevice.objects.all()
			district = districtBangladesh.objects.all()
			context 	= 	{'panda':my_phone,'success': 'Send Message Successfully','district':district,'navActive':'notification'}
			return render(request,'administration/notification.html',context)
			

	else:
		district = districtBangladesh.objects.all()
		context = {'panda':my_phone,"district":district,'navActive':'notification'}
		return render(request,'administration/notification.html',context)

@login_required(login_url='login_view')
def messagingList(request):

	if request.method == 'POST':
		search_text = request.POST['search_text']
		if search_text:
			data = Message_Notification_Read.objects.filter(Q(message__title__contains=search_text)
				| Q(message__message__contains=search_text) | Q(user_Message__username__contains=search_text))
			paginator = Paginator(data, 20)
			page = request.GET.get('page')
			contacts = paginator.get_page(page)
			context = {'panda':contacts,'navActive':'notification'}
			return render(request,'administration/notification_list_Search.html',context)
			
		else:
			data = Message_Notification_Read.objects.all()
			paginator = Paginator(data, 20)
			page = request.GET.get('page')
			contacts = paginator.get_page(page)
			context = {'panda':contacts,'navActive':'notification'}
			return render(request,'administration/notification_list_Search.html',context)

	data = Message_Notification_Read.objects.all()
	paginator = Paginator(data, 20)
	page = request.GET.get('page')
	contacts = paginator.get_page(page)
	context = {'panda':contacts,'navActive':'notification'}
	return render(request,'administration/notification_list.html',context)

@login_required(login_url='login_view')
def messagingListDelete(request):
	if request.user.is_admin:
		data = Message_Notification_Read.objects.all()
		data.delete()
	return redirect('messagingList')

@login_required(login_url='login_view')
def messagingListDeleteByID(request,id):
	if request.user.is_admin:
		data = Message_Notification_Read.objects.filter(id = id)
		data.delete()
	return redirect('messagingList')

@login_required(login_url='login_view')
def messagingListTwo(request):

	if request.method == 'POST':
		search_text = request.POST['search_text']

		if search_text:
			data = Message_Notification.objects.filter(Q(title__contains=search_text)
				| Q(message__contains=search_text) | Q(date__contains=search_text))
			paginator = Paginator(data, 20)
			page = request.GET.get('page')
			contacts = paginator.get_page(page)
			context = {'panda':contacts,'navActive':'notification'}
			return render(request,'administration/notification_listTwo_Search.html',context)
		else:
			data = Message_Notification.objects.all()
			paginator = Paginator(data, 20)
			page = request.GET.get('page')
			contacts = paginator.get_page(page)
			context = {'panda':contacts,'navActive':'notification'}
			return render(request,'administration/notification_listTwo_Search.html',context)

	data = Message_Notification.objects.all()
	paginator = Paginator(data, 20)
	page = request.GET.get('page')
	contacts = paginator.get_page(page)
	context = {'panda':contacts,'navActive':'notification'}
	return render(request,'administration/notification_listTwo.html',context)

@login_required(login_url='login_view')
def messagingListTwoDelete(request):
	if request.user.is_admin:
		data = Message_Notification.objects.all()
		data.delete()
	return redirect('messagingListTwo')

@login_required(login_url='login_view')
def messagingListTwoDeleteByID(request,id):
	if request.user.is_admin:
		data = Message_Notification.objects.filter(id=id)
		data.delete()
	return redirect('messagingListTwo')

# Districts Of Bangladesh
@login_required(login_url='login_view')
def districtsOFbangladesh(request):
	success = ""
	error = ""
	if request.method == "POST":
		district_name = request.POST["district_name"]
		product_point = request.POST["product_point"]
		try:
			data = districtBangladesh.objects.create(district_name=district_name.strip(" "),
				product_point=float(product_point))
			success = "Successfully Saved"
		except Exception as e:
			error = e


	data = districtBangladesh.objects.all().order_by("district_name")

	if success:
		context = {'panda':data,"success":success,'navActive':'administration'}
	elif error:
		context = {'panda':data,"error":error,'navActive':'administration'}
	else:
		context = {'panda':data,'navActive':'administration'}

	return render(request,'administration/districtBangladesh.html',context)

# Districts Of Bangladesh Delete
@login_required(login_url='login_view')
def districtsOFbangladesh_DeleteAll(request):
	if request.user.is_admin:
		data = districtBangladesh.objects.all().order_by("district_name")
		data.delete()
	return redirect('districtsOFbangladesh')

# Districts Of Bangladesh Delete by id
@login_required(login_url='login_view')
def districtsOFbangladesh_DeleteByID(request,id):
	if request.user.is_admin:
		data = districtBangladesh.objects.filter(id=id)
		data.delete()
	return redirect('districtsOFbangladesh')


# Bank of Bangladesh

@login_required(login_url='login_view')
def bankOFbangladesh(request):
	success = ""
	error = ""
	if request.method == "POST":
		bank_name = request.POST["bank_name"]
		try:
			data = bankListBangladesh.objects.create(bank_name=bank_name.strip(" "))
			success = "Successfully Saved"
		except Exception as e:
			error = e


	data = bankListBangladesh.objects.all().order_by("bank_name")

	if success:
		context = {'panda':data,"success":success,'navActive':'administration'}
	elif error:
		context = {'panda':data,"error":error,'navActive':'administration'}
	else:
		context = {'panda':data,'navActive':'administration'}

	return render(request,'administration/bankBangladesh.html',context)

# Bank Of Bangladesh Delete
@login_required(login_url='login_view')
def bankOFbangladesh_DeleteAll(request):
	if request.user.is_admin:
		data = bankListBangladesh.objects.all()
		data.delete()
	return redirect('bankOFbangladesh')

# Bank Of Bangladesh Delete by id
@login_required(login_url='login_view')
def bankOFbangladesh_DeleteByID(request,id):
	if request.user.is_admin:
		data = bankListBangladesh.objects.filter(id=id)
		data.delete()
	return redirect('bankOFbangladesh')