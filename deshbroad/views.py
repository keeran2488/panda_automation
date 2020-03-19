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
User = get_user_model()


from django.db.models import Q
from django.utils.crypto import get_random_string
from django.core import validators
from django.core.exceptions import ValidationError
from django.conf import settings
from datetime import datetime

from celery.result import AsyncResult
from deshbroad.forms import GenerateRandomUserForm
from deshbroad.tasks import activation_code_insert,activate_code_update

from django.db.models import Q

from cryptography.fernet import Fernet

from .models import activation_code
from accounts.models import (

	BonusRate,
	TechnicalSupport,
	OfferPage,
	MyDevice,
	MyUser,
	SaleInformation,
	offerType,
	districtBangladesh,
	Offer_Notification_Read,
	)


import pandas as pd
import xlwt
import random
import json
import numpy as np
import PIL
from PIL import Image
import dateutil.parser
from django.core.files.storage import FileSystemStorage
from accounts.code import codeKey,chekDatafram,dataWrap
key = codeKey()
dataframe = chekDatafram(key)

@login_required(login_url='login_view')
def index(request):
	saleuser = MyUser.objects.select_related('user_details').filter(Q(is_general_user=True) & Q(is_staff=False) & Q(is_admin=False)).distinct().annotate(num_sale=Count('saleinformation__activation')).order_by("-num_sale")[:6]
	
	saleInfo = SaleInformation.objects.all().order_by("-date")[:20]

	for infoData in saleInfo:
		cipher_suite = Fernet(key)
		infoData2 = cipher_suite.decrypt(infoData.activation.file.encode())
		infoData.activation.file = infoData2.decode("utf-8")


	dateNow = datetime.now()
	dateNow = dateNow.strftime("%A, %d-%m-%Y")
	# infoSalesActive = SaleInformation.objects.filter( Q(activation__active_check=True) & Q(activation__check=True) ).values('activation__active_check').annotate(Active_count=Count('activation__active_check')).distinct()
	# infoTotalsales 	= SaleInformation.objects.filter( Q(activation__check=True) & Q(activation__active_check=False) ).values('activation__check').annotate(Active_count=Count('activation__check')).distinct()
	infoSalesActive = activation_code.objects.filter( Q(active_check=True)).values('active_check').annotate(Active_count=Count('active_check')).distinct()
	# infoTotalsales 	= activation_code.objects.filter( Q(check=True) & Q(active_check=False) ).values('check').annotate(Active_count=Count('check')).distinct()
	infoTotalNew 	= activation_code.objects.filter( Q(active_check=False) ).values('active_check').annotate(Active_count=Count('active_check')).distinct()
	
	# yearSales = SaleInformation.objects.all().values('year').distinct().order_by("-year")
	
	# year = yearSales.first()

	dataSales_Count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	context ={"navActive":"index"}
	
	# if(request.method == "POST"):
	# 	year = int(request.POST["year"])

	# 	salesInyear = SaleInformation.objects.filter(year=year).values('month').annotate(product_count=Count('month')).distinct().order_by("-year")
	# 	for salesInyear in salesInyear:
	# 		dataSales_Count[int(salesInyear["month"])-1] = int(salesInyear["product_count"])
		
	# 	context = {
	# 		"panda":saleuser,
	# 		'infoTotalsales':infoTotalsales,
	# 		"infoSalesActive":infoSalesActive,
	# 		"infoTotalNew":infoTotalNew,
	# 		# "yearSales":yearSales,
	# 		"dataSales_Count":dataSales_Count,
	# 		"saleInfo":saleInfo,
	# 		"date":dateNow,
	# 		"navActive":"index",
	# 	}
	# 	print(dataSales_Count)
	# 	return HttpResponse(dataSales_Count)
		
	# else:
	# 	year = yearSales.first()
	# 	if year:
	# 		salesInyear = SaleInformation.objects.filter(year=year["year"]).values('month').annotate(product_count=Count('month')).distinct().order_by("-year")
	# 		for salesInyear in salesInyear:
	# 			dataSales_Count[int(salesInyear["month"])-1] = int(salesInyear["product_count"])
	context = {
		"panda":saleuser,
		# 'infoTotalsales':infoTotalsales,
		"infoSalesActive":infoSalesActive,
		"infoTotalNew":infoTotalNew,
			# "yearSales":yearSales,
		"dataSales_Count":dataSales_Count,
		"saleInfo":saleInfo,
		"date":dateNow,
		"navActive":"index",
		}
	return render(request, 'deshbroad/index.html',context)
		
	
	

@login_required(login_url='login_view')
def list_of_activation(request):

	infoSalesActive = activation_code.objects.filter(active_check=True).values('active_check').annotate(Active_count=Count('active_check')).distinct()
	infoTotalNew 	= activation_code.objects.filter(active_check=False).values('active_check').annotate(Active_count=Count('active_check')).distinct()
	
	# info = ""
	if request.method == 'POST':
		search_text = request.POST['search_text']

		if search_text:
			product_id = districtBangladesh.objects.only('id').filter(district_name__contains=search_text).first()
			info = activation_code.objects.filter(Q(date__contains=search_text) | Q(product_type=product_id)).values('date','product_type').annotate(activation_count=Count('file'),pendding_count=Count('id', filter= Q(active_check=False)),active_count=Count('id', filter = Q(active_check=True))).distinct().order_by("-product_type")
			paginator = Paginator(info, 20)
			page = request.GET.get('page')
			contacts = paginator.get_page(page)
			product = districtBangladesh.objects.all()
			context ={'panda':contacts,"navActive":"list_of_activation","product":product,}	
			return render(request, 'deshbroad/list_of_activation_Search.html',context)
		else:
			info = activation_code.objects.values('date','product_type').annotate(activation_count=Count('file'),pendding_count=Count('id', filter= Q(active_check=False)),active_count=Count('id', filter = Q(active_check=True))).distinct().order_by("-product_type")
			paginator = Paginator(info, 20)
			page = request.GET.get('page')
			contacts = paginator.get_page(page)
			product = districtBangladesh.objects.all()
			context ={'panda':contacts,"navActive":"list_of_activation","product":product,}
			return render(request, 'deshbroad/list_of_activation_Search.html',context)

	info = activation_code.objects.values('date','product_type').annotate(activation_count=Count('file'),pendding_count=Count('id', filter=Q(active_check=False)),active_count=Count('id', filter=Q(active_check=True))).distinct().order_by("-product_type")	
	product = districtBangladesh.objects.all()
	paginator = Paginator(info, 20)
	page = request.GET.get('page')
	contacts = paginator.get_page(page)

	context ={'panda':contacts,
	# 'infoTotalsales':infoTotalsales,
	"infoSalesActive":infoSalesActive,
	"infoTotalNew":infoTotalNew,
	"product":product,
	"navActive":"list_of_activation",
	}	
	return render(request, 'deshbroad/list_of_activation.html',context)


@login_required(login_url='login_view')
def upload_activation(request):
	product_data = districtBangladesh.objects.all()
	if(request.method == "POST"):
		# get value from the activation upload form
		product_name = request.POST.getlist('product_name')
		product_number = int(request.POST['total_product'])
		# product_date = datetime.now()
		# product_date = datetime.date.strptime(product_date, '%Y-%m-%d')

		countData=0
		count=0

		# product_details = product_name+" "+str(licence_type)+" PC "+str(licence_duration)+" Year"

		task = activation_code_insert.delay(product_name,product_number)
		return HttpResponse(json.dumps({'task_id': task.id}), content_type='application/json')
	context = {"navActive":"upload_activation","product_data":product_data}
	return render(request,'deshbroad/activation_upload.html',context)

@login_required(login_url='login_view')
def file_validation(request):
	if request.method == 'POST':
		form 			= request.FILES.getlist('chooseFile')
		try:
			for count, x in enumerate(form):
				def handle_uploaded_file(f):
					with open(settings.MEDIA_ROOT + 'code.txt', 'wb+') as destination:
						for chunk in f.chunks():
							destination.write(chunk)
				handle_uploaded_file(x)
			data = pd.read_csv(settings.MEDIA_ROOT + 'code.txt',header=None)
			data = str(data[0].count())+" PCs"
			# print(data)
		except Exception as e:
			data = e

	return HttpResponse(data)


@login_required(login_url="login_view")
def activation_code_details(request,date,product_type):

	info=""
	infoSalesActive = activation_code.objects.filter( Q(date=date) & Q(active_check=True) & Q(product_type=product_type) ).values('active_check').annotate(Active_count=Count('active_check')).distinct()
	# infoTotalsales 	= activation_code.objects.filter( Q(batch_code=batch_code) & Q(check=True) & Q(active_check=False) ).values('check').annotate(Active_count=Count('check')).distinct()
	infoTotalNew 	= activation_code.objects.filter( Q(date=date) & Q(active_check=False) & Q(product_type=product_type) ).values('active_check').annotate(Active_count=Count('active_check')).distinct()

	if request.method == 'POST':
		search_text = request.POST['search_text']

		if search_text:

			checkData = dataframe[dataframe['file2'] == search_text]
			if checkData.empty:
				search_text = search_text
			else:
				search_text = checkData['file'].values[0]

			if search_text.upper() == "SCAN":
				info = activation_code.objects.filter(Q(date=date) & Q(
				Q(file__contains=search_text) | Q(active_check=True))).order_by("-id")[0:20]


			elif search_text.upper() == "NEW":
				info = activation_code.objects.filter(Q(date=date) & Q(
				Q(file__contains=search_text) | Q(active_check=False))).order_by("-id")[0:20]

			else:
				info = info = activation_code.objects.filter(Q(date=date) & Q(
				Q(file__contains=search_text))).order_by("-id")[0:20]

			for data in info:
				cipher_suite = Fernet(key)
				dataActive = cipher_suite.decrypt(data.file.encode())
				data.file = dataActive.decode("utf-8")

			context ={'panda':info,"date":date,
			"product_type":product_type,"infoSalesActive":infoSalesActive,
			"infoTotalNew":infoTotalNew}
			return render(request, 'deshbroad/activation_code_details_Search.html',context)
		else:
			info = activation_code.objects.filter(Q(date=date) & Q(product_type=product_type)).order_by("-id")
			for data in info:
				cipher_suite = Fernet(key)
				dataActive = cipher_suite.decrypt(data.file.encode())
				data.file = dataActive.decode("utf-8")

			paginator = Paginator(info, 20)
			page = request.GET.get('page')
			contacts = paginator.get_page(page)

			context ={'panda':contacts,"date":date,
			"product_type":product_type,
			# 'infoTotalsales':infoTotalsales,
			"infoSalesActive":infoSalesActive,
			"infoTotalNew":infoTotalNew,
			"navActive":"list_of_activation"}
			return render(request, 'deshbroad/activation_code_details_Search.html',context)

	info = activation_code.objects.filter(Q(date=date) & Q(product_type=product_type)).order_by("-id")
	for data in info:
		cipher_suite = Fernet(key)
		dataActive = cipher_suite.decrypt(data.file.encode())
		data.file = dataActive.decode("utf-8")
	paginator = Paginator(info, 20)
	page = request.GET.get('page')
	contacts = paginator.get_page(page)

	context ={'panda':contacts,"date":date,
	"product_type":product_type,
	# 'infoTotalsales':infoTotalsales,
	"infoSalesActive":infoSalesActive,
	"infoTotalNew":infoTotalNew,
	"navActive":"list_of_activation"}
	return render(request, 'deshbroad/activation_code_details.html',context)
	
# Export Section
@login_required(login_url='login_view')
def export_users_xls(request):
	if request.user.is_admin:
		response = HttpResponse(content_type='application/ms-excel')
		response['Content-Disposition'] = 'attachment; filename="QRCode.xls"'

		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet('Users')

		# Sheet header, first row
		row_num = 0

		font_style = xlwt.XFStyle()
		font_style.font.bold = True

		columns = ['Code', 'Product Type', 'QR Code']

		for col_num in range(len(columns)):
			ws.write(row_num, col_num, columns[col_num], font_style)

		# Sheet body, remaining rows
		font_style = xlwt.XFStyle()
		al = xlwt.Alignment()
		al.wrap = xlwt.Alignment.WRAP_AT_RIGHT
		font_style.alignment = al

		rows = activation_code.objects.all().values_list('file', 'product_type__district_name','date')

		# for data in rows:
		# 	cipher_suite = Fernet(key)
		# 	dataActive = cipher_suite.decrypt(data[0].encode())
		# 	data[0] = dataActive.decode("utf-8")

		col_width = 256 * 35

		image_width = 100.0
		image_height = 182.0

		cell_width = 100.0
		cell_height = 20.0

		x_scale = cell_width/image_width
		y_scale = cell_height/image_height

		for row in rows:
			row_num += 1

			for col_num in range(len(row)):
				# print(row[col_num])
				ws.row(row_num).height_mismatch = True
				ws.row(row_num).height = 256*10
				ws.col(col_num).width = col_width
				if col_num == 2:
					with open (dataWrap(row,col_num,key), "rb") as bmpfile:
						bmpdata = bmpfile.read()
						ws.insert_bitmap_data(bmpdata, row_num, col_num,x=0,y=0, scale_x = x_scale, scale_y = y_scale)
					# ws.insert_bitmap(dataWrap(row,col_num,key), row_num, col_num)
				else:
					ws.write(row_num, col_num, str(dataWrap(row,col_num,key)), font_style)

		wb.save(response)
		return response
	return redirect('list_of_activation')


@login_required(login_url='login_view')
def export_users_xls_batchCode(request,date,product_type):
	if request.user.is_admin:
		response = HttpResponse(content_type='application/ms-excel')
		response['Content-Disposition'] = 'attachment; filename='+date+".xls"

		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet('Users')

		# Sheet header, first row
		row_num = 0

		font_style = xlwt.XFStyle()
		font_style.font.bold = True

		columns = ['Code', 'Product Type', 'QR Code']

		for col_num in range(len(columns)):
			ws.write(row_num, col_num, columns[col_num], font_style)

		# Sheet body, remaining rows
		font_style = xlwt.XFStyle()

		rows = activation_code.objects.filter(date=date,product_type=product_type).values_list('file', 'product_type__district_name','date')

		# for data in rows:
		# 	cipher_suite = Fernet(key)
		# 	dataActive = cipher_suite.decrypt(data[0].encode())
		# 	data[0] = dataActive.decode("utf-8")

		col_width = 256 * 35

		image_width = 100.0
		image_height = 182.0

		cell_width = 100.0
		cell_height = 20.0

		x_scale = cell_width/image_width
		y_scale = cell_height/image_height

		for row in rows:
			row_num += 1

			for col_num in range(len(row)):
				# print(row[col_num])
				ws.row(row_num).height_mismatch = True
				ws.row(row_num).height = 256*10
				ws.col(col_num).width = col_width
				if col_num == 2:
					with open (dataWrap(row,col_num,key), "rb") as bmpfile:
						bmpdata = bmpfile.read()
						ws.insert_bitmap_data(bmpdata, row_num, col_num,x=0,y=0, scale_x = x_scale, scale_y = y_scale)
					# ws.insert_bitmap(dataWrap(row,col_num,key), row_num, col_num)
				else:
					ws.write(row_num, col_num, str(dataWrap(row,col_num,key)), font_style)

		wb.save(response)
		return response
	return redirect('list_of_activation')

@login_required(login_url='login_view')
def get_task_info(request):
    task_id = request.GET.get('task_id', None)
    if task_id is not None:
        task = AsyncResult(task_id)
        data = {
            'state': task.state,
            'result': task.result,
        }
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
    	return HttpResponse('No job id given.')



# Bonus Rate
@login_required(login_url="login_view")
def bonusRate(request):
	if request.method == 'POST':
		bonus_Rate = request.POST['bonusRate']
		data = BonusRate.objects.filter(id=1).update(bonus_per_rate=bonus_Rate)
		if data:
			data = BonusRate.objects.filter(id=1)
			context = {'panda':data,'success':'Update Bonus Rate',"navActive":"bonusRate"}
			return render(request, 'deshbroad/bonusRate.html',context)
		else:
			data = BonusRate.objects.filter(id=1)
			context = {'panda':data,'error':'Update Error',"navActive":"bonusRate"}
			return render(request, 'deshbroad/bonusRate.html',context)

	data = BonusRate.objects.filter(id=1)
	context = {'panda':data,"navActive":"bonusRate"}
	return render(request, 'deshbroad/bonusRate.html',context)


# Technical Support
@login_required(login_url="login_view")
def technicalSupport(request):
	if request.method == 'POST':
		phone_number 	= request.POST['phone_number']
		email			= request.POST['email']
		data = TechnicalSupport.objects.filter(id=1).update(phone_number=phone_number,email=email)
		if data:
			data = TechnicalSupport.objects.filter(id=1)
			context = {'panda':data,'success':'Update Bonus Rate',"navActive":"techSupport"}
			return render(request, 'deshbroad/techSupport.html',context)
		else:
			data = TechnicalSupport.objects.filter(id=1)
			context = {'panda':data,'error':'Update Error',"navActive":"techSupport"}
			return render(request, 'deshbroad/techSupport.html',context)

	data = TechnicalSupport.objects.filter(id=1)
	context = {'panda':data,"navActive":"techSupport"}
	return render(request, 'deshbroad/techSupport.html',context)



# offers
@login_required(login_url="login_view")
def offersPage(request):
	my_phone = MyDevice.objects.all()
	if request.method == 'POST':
		imageOne 		= request.FILES.get('image')
		reward_details	= request.POST['reward_details']
		userSelect 		= request.POST.getlist('userSelect')

		data = {}
		data['message'] = reward_details
		data['title'] = "New Reward For You.."
		json_data = json.dumps(data)

		if imageOne is not None:
			imageOne = image_upload_for_offer(imageOne)

			qry = OfferPage.objects.create(image_offer=imageOne,image_details=reward_details)
			qry.save()
			if userSelect:
				for userID in userSelect:
					my_phone 	= MyDevice.objects.filter(Q(user=userID) & Q(is_active=True))
					userMy 		= MyUser.objects.only('id').get(id=userID)
					readMez		= Offer_Notification_Read.objects.create(user_Message=userMy,offers=qry)
					readMez.save()	
					my_phone.send_message({'messages': json_data}, collapse_key='something')
				typeData = offerType.objects.all()
				context = {'success': 'Send..','offerType':typeData,"navActive":"offersPage"}
				data = {}
				
				MyDevice.objects.filter(is_active=True).send_message({'messages': json_data}, collapse_key='something')
				return render(request,'offer/uploadoffer.html',context)
			else:
				my_phone = MyDevice.objects.filter(is_active=True)
				for my_phone in my_phone:
					userMy = MyUser.objects.only('id').get(id=my_phone.user.id)
					readMez = Offer_Notification_Read.objects.create(user_Message=userMy,offers=qry)
					readMez.save()
				MyDevice.objects.filter(is_active=True).send_message({'messages': json_data}, collapse_key='something')

			if qry:

				typeData = offerType.objects.all()
				context = {'success': 'upload offer','offerType':typeData,"navActive":"offersPage"}
				data = {}
				data['message'] = 'Please Check Your Reward Option'
				data['title'] = "Reward"
				json_data = json.dumps(data)
				MyDevice.objects.filter(is_active=True).send_message({'messages': json_data}, collapse_key='something')
				return render(request,'offer/uploadoffer.html',context)

			else:
				typeData = offerType.objects.all()
				context = {'exception': 'Somethink Wrong to upload','offerType':typeData,"navActive":"offersPage"}
				return render(request,'offer/uploadoffer.html',context)
		else:
			context = {'exception': 'Somethink Wrong to upload',"navActive":"offersPage"}
			return render(request,'offer/uploadoffer.html',context)		
	
	typeData = offerType.objects.all()
	context = {'panda':my_phone,'offerType':typeData,"navActive":"offersPage"}
	return render(request,'offer/uploadoffer.html',context)


# Offer list
def offerList(request):
	data =  OfferPage.objects.all()
	context = {'panda':data,"navActive":"offersPage"}
	return render(request,'offer/offerlist.html',context)



def image_upload_for_offer(filename):

	file = filename.name
	filebase, extension = file.split(".")
	file = random.randint(1,10000)*5
	image_name = "%s.%s"%(file,extension)
	try:
		def handle_uploaded_file(f):
			with open(settings.MEDIA_ROOT + image_name, 'wb+') as destination:
				for chunk in f.chunks():
					destination.write(chunk)
		handle_uploaded_file(filename)
	except Exception as e:
		print(e)

	return image_name


# delete Section
@login_required(login_url="login_view")
def delete_all_activation_batch(request):
	if request.user.is_admin:
		data = activation_code.objects.all()
		data.delete()
		return redirect('list_of_activation')
	return redirect('list_of_activation')

@login_required(login_url="login_view")
def delete_activation_batch(request,date,product_type):
	if request.user.is_admin:
		data = activation_code.objects.filter(Q(product_type=product_type) & Q(date=date))
		data.delete()
		return redirect('list_of_activation')
	return redirect('list_of_activation')

@login_required(login_url="login_view")
def delete_activation_batchCode(request,file,date,product_type):
	if request.user.is_admin:
		checkData = dataframe[dataframe['file2'] == file]
		file = checkData['file'].values[0]
		data = activation_code.objects.filter(file=file)
		data.delete()
		return redirect('activation_code_details',date=date,product_type=product_type)
	return redirect("")

@login_required(login_url="login_view")
def delete_offers(request,id):
	if request.user.is_admin:
		data = OfferPage.objects.filter(id=id)
		data.delete()
		return redirect('offerList')
	return redirect('offerList')

def delete_offers_all(request):
	if request.user.is_admin:
		data = OfferPage.objects.all()
		data.delete()
		return redirect('offerList')
	return redirect('offerList')


# Search
@login_required(login_url='login_view')
def search_activation(request):
	if request.method == 'POST':
		search_text = request.POST['search_text']
		if search_text!='':
			info = activation_code.objects.filter(Q(Q(username__contains=search_text) | Q(full_name__contains=search_text)) & Q(Q(is_general_user=True) & Q(is_staff=False) & Q(is_admin=False)) )[:50]
		else:
			info = activation_code.objects.select_related('user_details').filter(Q(is_general_user=True) & Q(is_staff=False) & Q(is_admin=False) )[:9]
	else:
		info = activation_code.objects.select_related('user_details').filter(Q(is_general_user=True) & Q(is_staff=False) & Q(is_admin=False) )[:9]
	
	context ={'panda':info}
	return render(request,'saleUser/saleUserSearch.html',context)

# Profile
@login_required(login_url='login_view')
def myProfile(request):

	if request.method == 'POST':
		try:
			usename 	= request.POST['username']
			email 		= request.POST['email']
			full_name 	= request.POST['full_name']
			image 		= request.FILES.get('image')


			if image is not None:
				image = image_upload_admin(image,request.user.username)
				print(image)
				qry = MyUser.objects.filter(id=request.user.id).update(username=usename,email=email, full_name=full_name,image=image)
			else:
				qry = MyUser.objects.filter(id=request.user.id).update(username=usename,email=email, full_name=full_name,)


			if qry:
				info = MyUser.objects.filter(id=request.user.id)
				context = {'panda':info,'success': 'Updated Data'}
				return render(request,'deshbroad/editProfile.html',context)

		except Exception as e:
			info = MyUser.objects.filter(id=request.user.id)
			context = {'exception':e,'panda':info}
			return render(request,'deshbroad/editProfile.html',context)

	info = MyUser.objects.filter(id=request.user.id)
	context = {"panda":info}
	return render(request,'deshbroad/editProfile.html',context)


@login_required(login_url='login_view')
def password_reset_admin(request):
	if request.method == "POST":
		passwordReset = request.POST['passwordReset']
		users = User.objects.get(pk=request.user.id)
		users.set_password(passwordReset)
		users.save()
		return redirect('myProfile')
	return render(request,'saleUser/resetPass.html')


def image_upload_admin(filename,user):
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



# Offers 
@login_required(login_url="login_view")
def OfferType(request):
	if request.method == 'POST':

		offerTypeOne 	= request.POST['offerType1']
		offerTypeTwo 	= request.POST['offerType2']
		offerTypethree 	= request.POST['offerType3']

		data = offerType.objects.filter(id=1).update(offer_name=offerTypeOne)
		data2 = offerType.objects.filter(id=2).update(offer_name=offerTypeTwo)
		data3 = offerType.objects.filter(id=3).update(offer_name=offerTypethree)
		
		if data and data2 and data3:

			data = offerType.objects.filter(id=1)
			data2 = offerType.objects.filter(id=2)
			data3 = offerType.objects.filter(id=3)

			context = {'panda':data,'panda2':data2,'panda3':data3,'success':'Update Offers Type',"navActive":"offersPage"}
			return render(request, 'deshbroad/offerType.html',context)
		else:
			data = offerType.objects.filter(id=1)
			data2 = offerType.objects.filter(id=2)
			data3 = offerType.objects.filter(id=3)

			context = {'panda':data,'panda2':data2,'panda3':data3,'error':'Update Error',"navActive":"offersPage"}
			return render(request, 'deshbroad/offerType.html',context)

	data = offerType.objects.filter(id=1)
	data2 = offerType.objects.filter(id=2)
	data3 = offerType.objects.filter(id=3)
	context = {'panda':data,'panda2':data2,'panda3':data3,"navActive":"offersPage"}
	return render(request, 'deshbroad/offerType.html',context)

# Active Code Upload
@login_required(login_url='login_view')
def activate_code_upload(request):
	if request.method == 'POST':
		# chooseFile = request.FILES['chooseFile']
		task = activate_code_update.delay()
		return HttpResponse(json.dumps({'task_id': task.id}), content_type='application/json')
	context = {"navActive":"activate_code_upload"}
	return render(request,'deshbroad/activate_code_upload.html',context)



# execel File Activation
@login_required(login_url='login_view')
def excel_file(request):
	if request.user.is_admin and request.user.is_staff and request.user.is_general_user:
		length = ""
		if request.method == 'POST' and request.FILES['excelFile']:
			excel_file = request.FILES['excelFile']
			fs = FileSystemStorage()
			# length = pd.read_excel(excel_file.read())
			# filePath = handle_uploaded_file(excel_file)
			df = pd.read_excel(excel_file)
			columns = ['Activation code', 'Sales Code', 'Promo Code', 'Date','Batch Code', 'Product Type']
			# activation_code = pd.read_excel(excel_file)[columns[0]]
			# sales_code 		= pd.read_excel(excel_file)[columns[1]]
			# promo_code 		= pd.read_excel(excel_file)[columns[2]]
			# date 	   		= pd.read_excel(excel_file)[columns[3]]
			# batch_code 	  	= pd.read_excel(excel_file)[columns[4]]
			# product_type 	= pd.read_excel(excel_file)[columns[5]]
			j = 0;
			for i in df.index:
				batch_code=df[columns[4]][i]

				cipher_suite = Fernet(key)
				activationData = cipher_suite.encrypt(df[columns[0]][i].encode())
				file = activationData.decode("utf-8")

				sales_code=df[columns[1]][i]
				customer_code=df[columns[2]][i]
				date=df[columns[3]][i]
				product_type=df[columns[5]][i]
				j+=1;
				activation_code.objects.create(batch_code=batch_code,file=file,
					sales_code=sales_code,customer_code=customer_code, date=dateutil.parser.parse(date),
					product_type=product_type,check=0)

			# if i == j:
			# 	length = j
			# else:
			# 	length = "jas"
			
			# length = activation_code[0]
		context = {'length':length,"navActive":"excel_file"}
		return render(request,'deshbroad/excel_file_upload.html',context)

@login_required(login_url='login_view')
def file_validation_two(request):
	length = 0
	if request.method == 'POST':
		form 			= request.FILES['chooseFile']
		path = handle_uploaded_file(form)
		activation_code = pd.read_excel(path)['Activation code']
		length = len(activation_code)
	return HttpResponse(length)

def handle_uploaded_file(f):
    with open(settings.MEDIA_ROOT + 'activeCode.xls', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return settings.MEDIA_ROOT + 'activeCode.xls'


# HTTP Error 400
def bad_request(request):
    return render(request,"404/404_page.html")