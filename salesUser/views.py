import os
from django.conf import settings
from django.shortcuts import render , redirect
from django.http import HttpResponse
from salesUser.forms import SalesRegistrationForm
from accounts.models import SalesProfile,MyUser,SaleInformation,districtBangladesh,bankListBangladesh
from django.db.models import Count,Sum
from django.contrib.auth.decorators import login_required

from django.db.models import Q

from django.contrib.auth import get_user_model

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import pandas as pd
import xlwt
from cryptography.fernet import Fernet
from accounts.code import codeKey,chekDatafram,dataWrap
key = codeKey()
dataframe = chekDatafram(key)

User = get_user_model()

@login_required(login_url='login_view')
def createSales(request):
	if request.method=='POST':
		form = SalesRegistrationForm(request.POST,request.FILES)
		try:
			if form.is_valid():
				form.image = form.cleaned_data["image"]
				form.save()
				form = SalesRegistrationForm()
				context = 	{'form':form,'success': 'Saved Data',"navActive":"createSales"}
				return render(request,'saleUser/create_sales_user.html',context)
			else:
				context = 	{'form':form,"navActive":"createSales"}
				return render(request,'saleUser/create_sales_user.html',context)

		except Exception as e:
			form = SalesRegistrationForm()
			context = {'errorCreate':e,'form':form,"navActive":"createSales"}
			return render(request,'saleUser/create_sales_user.html',context)
			
	
	form = SalesRegistrationForm()
	context = 	{'form':form,"navActive":"createSales"}
	return render(request,'saleUser/create_sales_user.html',context)

@login_required(login_url='login_view')
def listOfSales(request):
	saleuser = MyUser.objects.select_related('user_details').filter(Q(is_general_user=True) & Q(is_staff=False) & Q(is_admin=False)).distinct().annotate(num_sale=Count('saleinformation__activation'))
	
	paginator = Paginator(saleuser, 9)
	page = request.GET.get('page')
	contacts = paginator.get_page(page)
	context = {'panda': contacts,"navActive":'listOfSales'}
	return render(request,'saleUser/userList.html',context)


@login_required(login_url='login_view')
def salesOfSales(request):
	saleuser = SaleInformation.objects.all()
	
	for infoData in saleuser:
		cipher_suite = Fernet(key)
		dataActive = cipher_suite.decrypt(infoData.activation.file.encode())
		infoData.activation.file = dataActive.decode("utf-8")

	paginator = Paginator(saleuser, 25)

	page = request.GET.get('page')
	contacts = paginator.get_page(page)
	context = {'panda': contacts,"navActive":'salesOfSales'}
	return render(request,'saleUser/sale.html',context)


@login_required(login_url='login_view')
def editSaleProfile(request,id):
	if request.method == 'POST':
		try:
			usename 	= request.POST['username']
			email 		= request.POST['email']
			full_name 	= request.POST['full_name']
			image 		= request.FILES.get('image')
			phn_num 		= request.POST['phn_num']
			company_add 	= request.POST['company_add']

			if image is not None:
				image = image_upload(image,usename)
				print(image)
				qry = MyUser.objects.filter(pk=id).update(username=usename,email=email, full_name=full_name,image=image)
			else:
				qry = MyUser.objects.filter(pk=id).update(username=usename,email=email, full_name=full_name,)

			qry2 = SalesProfile.objects.filter(sales_user=id).update(company_address=company_add,
					phone_number=phn_num)

			if qry & qry2:
				saleuser = MyUser.objects.filter(pk=id)
				context = {'panda':saleuser,'success': 'Updated Data',
				"navActive":'editSaleProfile'}
				return render(request,'saleUser/editProfile.html',context)

		except Exception as e:
			saleuser = MyUser.objects.filter(pk=id)
			context = {'exception':e,'panda':saleuser,"navActive":'editSaleProfile'}
			return render(request,'saleUser/editProfile.html',context)

	saleuser = MyUser.objects.filter(pk=id)
	context = {'panda':saleuser,"navActive":'editSaleProfile'}
	return render(request,'saleUser/editProfile.html',context)

# Delete
@login_required(login_url='login_view')
def delete_saleProfile(request,id):
	if request.user.is_admin:
		data = MyUser.objects.filter(pk=id)
		data.delete()
		return redirect('listOfSales')
	return redirect('listOfSales')

@login_required(login_url='login_view')
def delete_saleInfo(request,id):
	if request.user.is_admin:
		data = SaleInformation.objects.filter(pk=id)
		data.delete()
		return redirect('salesOfSales')
	return redirect('salesOfSales')

@login_required(login_url='login_view')
def delete_saleProfile_all(request):
	if request.user.is_admin:
		data = MyUser.objects.filter(Q(is_general_user=True) & Q(is_staff=False) & Q(is_admin=False) )
		data.delete()
		return redirect('listOfSales')
	return redirect('listOfSales')

@login_required(login_url='login_view')
def delete_salesInfo_all(request):
	if request.user.is_admin:
		data = SaleInformation.objects.all()
		data.delete()
		return redirect('salesOfSales')
	return redirect('salesOfSales')

def image_upload(filename,user):
	file = filename.name
	filebase, extension = file.split(".")
	# file_extension = file.endswith(".jpg")
	try:
		os.mkdir(os.path.join(settings.MEDIA_ROOT, str(user)))
	except Exception as e:
		print(e)

	
	image_name = "%s/%s.%s"%(user,user,extension)
	try:
		def handle_uploaded_file(f):
			with open(settings.MEDIA_ROOT + image_name, 'wb+') as destination:
				for chunk in f.chunks():
					destination.write(chunk)
		handle_uploaded_file(filename)
	except Exception as e:
		print(e)

	return image_name

@login_required(login_url='login_view')
def password_reset(request,id):
	if request.method == "POST":
		passwordReset = request.POST['passwordReset']
		users = User.objects.get(pk=id)
		users.set_password(passwordReset)
		users.save()
		return redirect('listOfSales')
	context = {"navActive":'editSaleProfile'}
	return render(request,'saleUser/resetPass.html',context)

# Search
@login_required(login_url='login_view')
def search_salesUser(request):
	if request.method == 'POST':
		search_text = request.POST['search_text']
		if search_text!='':
			info = MyUser.objects.filter(Q(Q(username__contains=search_text) | Q(full_name__contains=search_text)) & Q(Q(is_general_user=True) & Q(is_staff=False) & Q(is_admin=False)) )[:50]
		else:
			info = MyUser.objects.select_related('user_details').filter(Q(is_general_user=True) & Q(is_staff=False) & Q(is_admin=False) )[:9]
	else:
		info = MyUser.objects.select_related('user_details').filter(Q(is_general_user=True) & Q(is_staff=False) & Q(is_admin=False) )[:9]
	
	context ={'panda':info}
	return render(request,'saleUser/saleUserSearch.html',context)


@login_required(login_url='login_view')
def search_saleInfo(request):
	if request.method == 'POST':
		search_text = request.POST['search_text']
		if search_text!='':
			checkData = dataframe[dataframe['file2'] == search_text]
			if checkData.empty:
				search_text = search_text
			else:
				search_text = checkData['file'].values[0]

			info = SaleInformation.objects.filter(Q(activation__file__contains=search_text) 
				| Q(user__full_name__contains=search_text) | Q(user__username__contains=search_text) )[:50]
		else:
			info = SaleInformation.objects.all()[:25]

	else:
		info = SaleInformation.objects.all()[:25]

	for infoData in info:
		cipher_suite = Fernet(key)
		dataActive = cipher_suite.decrypt(infoData.activation.file.encode())
		infoData.activation.file = dataActive.decode("utf-8")

	context ={'panda':info}
	return render(request,'saleUser/saleInfoSearch.html',context)


# User data Export
@login_required(login_url='login_view')
def export_users_xl_sales(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="Sales User.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Users')

	# Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Name','Username','E-mail','Company Name','Phone Number','Company Address','Payment Account']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	# Sheet body, remaining rows
	font_style = xlwt.XFStyle()

	rows = MyUser.objects.select_related('user_details').filter(Q(is_general_user=True) & Q(is_staff=False) & Q(is_admin=False) ).values_list('full_name',
		'username','email','user_details__company_name','user_details__phone_number','user_details__company_address',
		'user_details__payment_account',)

	for row in rows:
		row_num += 1
		for col_num in range(len(row)):
			# print(row[col_num])
			ws.write(row_num, col_num, str(row[col_num]), font_style)

	wb.save(response)
	return response


@login_required(login_url='login_view')
def export_users_xl_salesInfo(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="Sales Information.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Users')

	# Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['activation','Sale Man','Date','Customer Name','Customer Phone Number','Address']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	# Sheet body, remaining rows
	font_style = xlwt.XFStyle()

	rows = SaleInformation.objects.all().values_list('activation__file',
		'user__full_name','date','buyerName','phoneNumber','address')

	for row in rows:
		row_num += 1
		for col_num in range(len(row)):
			# print(row[col_num])
			ws.write(row_num, col_num, str(row[col_num]), font_style)

	wb.save(response)
	return response


# sales Details for user
def salesInfoForUser(request,id):

	infoSalesActive = SaleInformation.objects.filter( Q(user__id=id) & Q(activation__active_check=True) ).values('activation__active_check').annotate(Active_count=Count('activation__active_check')).distinct()
	infoTotalsales 	= SaleInformation.objects.filter( Q(user__id=id) & Q(activation__active_check=True) ).values('product__district_name').annotate(Active_point=Sum('product__product_point'))

	if request.method == 'POST':
		search_text = request.POST['search_text']
		if search_text:

			checkData = dataframe[dataframe['file2'] == search_text]
			if checkData.empty:
				search_text = search_text
			else:
				search_text = checkData['file'].values[0]

			saleuser = SaleInformation.objects.filter(Q(user__id=id) & Q(Q(activation__file__contains=search_text) 
				| Q(user__full_name__contains=search_text) | Q(user__username__contains=search_text)))[:50]

			# SaleInformation.objects.filter(Q(activation__file__contains=search_text) 
			# 	| Q(user__full_name__contains=search_text) | Q(user__username__contains=search_text) )[:50]

			for infoData in saleuser:
				cipher_suite = Fernet(key)
				dataActive = cipher_suite.decrypt(infoData.activation.file.encode())
				infoData.activation.file = dataActive.decode("utf-8")

			paginator = Paginator(saleuser, 20)
			page = request.GET.get('page')
			contacts = paginator.get_page(page)
			context = {'panda': contacts,'id':id,"infoSalesActive":infoSalesActive,
			"infoTotalsales":infoTotalsales,"navActive":'editSaleProfile'}
			return render(request,'saleUser/saleUserSalesInfo_Search.html',context)
		else:
			saleuser = SaleInformation.objects.filter(user__id=id)
			for infoData in saleuser:
				cipher_suite = Fernet(key)
				dataActive = cipher_suite.decrypt(infoData.activation.file.encode())
				infoData.activation.file = dataActive.decode("utf-8")
			paginator = Paginator(saleuser, 20)
			page = request.GET.get('page')
			contacts = paginator.get_page(page)
			context = {'panda': contacts,'id':id,"infoSalesActive":infoSalesActive,
			"infoTotalsales":infoTotalsales,"navActive":'editSaleProfile'}
			return render(request,'saleUser/saleUserSalesInfo_Search.html',context)

	saleuser = SaleInformation.objects.filter(user__id=id)
	for infoData in saleuser:
		cipher_suite = Fernet(key)
		dataActive = cipher_suite.decrypt(infoData.activation.file.encode())
		infoData.activation.file = dataActive.decode("utf-8")
	paginator = Paginator(saleuser, 20)
	page = request.GET.get('page')
	contacts = paginator.get_page(page)
	context = {'panda': contacts,'id':id,"infoSalesActive":infoSalesActive,
	"infoTotalsales":infoTotalsales,"navActive":'editSaleProfile'}			
	return render(request,'saleUser/saleUserSalesInfo.html',context)

