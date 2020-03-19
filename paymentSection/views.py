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

from django.db.models import Q

from product_showcase.models import Product_Type,Product_Speciality,Product_list
from product_showcase.forms import Product_Showcase_form
from paymentSection.models import PaymentGatwayModel

from accounts.models import (MyUser,MyDevice,Message_Notification,SalesProfile,SaleInformation,
	Message_Notification_Read,Message_Notification,districtBangladesh,bankListBangladesh,BonusRate)

import json
import pandas as pd
import xlwt


def paymentGateway(request):
	my_phone = MyDevice.objects.all()
	unitRate = BonusRate.objects.values("bonus_per_rate").filter(id=1)[0]

	total_activate_paid = 0
	current_paid = 0
	padding = 0
	active = 0
	total_taka = 0

	if request.method == 'POST':
		# Device = get_device_model()
		message 		= request.POST['message']
		# title 			= request.POST['titel']
		userSelect 		= request.POST.getlist('userSelect')
		DistrictSelect 	= request.POST.getlist('districtSelect')

		data = {}
		data['message'] = message
		data['title'] = "Payment"
		json_data = json.dumps(data)


		if DistrictSelect:

			for DistrictSelect in DistrictSelect:
				data2 = SalesProfile.objects.filter(district_name = DistrictSelect)
				for data2 in data2:
					my_phone = MyDevice.objects.filter(Q(user=data2.sales_user.id) & Q(is_active=True))
					userMy 				= MyUser.objects.only('id').get(id=data2.sales_user.id)
					infoSalesActive 	= SaleInformation.objects.filter( Q(user__id=data2.sales_user.id) & Q(activation__active_check=True) & Q(activation__check=True) ).values('activation__active_check').annotate(Active_count=Count('activation__active_check')).distinct()
					infoTotalpadding 	= SaleInformation.objects.filter( Q(user__id=data2.sales_user.id) & Q(activation__check=True) & Q(activation__active_check=False) ).values('activation__check').annotate(Active_count=Count('activation__check')).distinct()

					payment = PaymentGatwayModel.objects.values('total_activate_paind').filter(salesUser=userMy).order_by('-id')

					if payment:
						total_activate_paid = int(payment[0]["total_activate_paind"])
					if infoTotalpadding:
						padding = int(infoTotalpadding[0]['Active_count'])
					if infoSalesActive:
						active  = int(infoSalesActive[0]['Active_count'])

					if active>total_activate_paid:
						current_paid = active - total_activate_paid
						total_activate_paid = current_paid + total_activate_paid
						total_taka = current_paid * float(unitRate['bonus_per_rate'])
					else:
						total_activate_paid = total_activate_paid
						current_paid = 0
						total_taka = current_paid * float(unitRate['bonus_per_rate'])

					payment = PaymentGatwayModel.objects.create(salesUser=userMy,
						total_activate_paind=total_activate_paid,current_paid=current_paid,
						unit_rate=float(unitRate['bonus_per_rate']),total_taka=total_taka,massage=message)
					if payment:
						# my_phone = MyDevice.objects.all()
						district = districtBangladesh.objects.all()
						my_phone.send_message({'messages': json_data}, collapse_key='something')
						context 	= 	{'panda':my_phone,'success': 'Payment Message Send Successfully',
						'district':district,"navActive":"payment"}
						return render(request,'paymentSection/payment_gateway_template.html',context)		

		else:
			
			if userSelect:
				for userID in userSelect:
					my_phone = MyDevice.objects.filter(Q(user=userID) & Q(is_active=True))
					userMy = MyUser.objects.only('id').get(id=userID)
					infoSalesActive 	= SaleInformation.objects.filter( Q(user__id=userID) & Q(activation__active_check=True) & Q(activation__check=True) ).values('activation__active_check').annotate(Active_count=Count('activation__active_check')).distinct()
					infoTotalpadding 	= SaleInformation.objects.filter( Q(user__id=userID) & Q(activation__check=True) & Q(activation__active_check=False) ).values('activation__check').annotate(Active_count=Count('activation__check')).distinct()

					payment = PaymentGatwayModel.objects.values('total_activate_paind').filter(salesUser=userMy).order_by('-id')

					if payment:
						total_activate_paid = int(payment[0]["total_activate_paind"])
					if infoTotalpadding:
						padding = int(infoTotalpadding[0]['Active_count'])
					if infoSalesActive:
						active  = int(infoSalesActive[0]['Active_count'])

					if active>total_activate_paid:
						current_paid = active - total_activate_paid
						total_activate_paid = current_paid + total_activate_paid
						total_taka = current_paid * float(unitRate['bonus_per_rate'])
					else:
						total_activate_paid = total_activate_paid
						current_paid = 0
						total_taka = current_paid * float(unitRate['bonus_per_rate'])

					payment = PaymentGatwayModel.objects.create(salesUser=userMy,
						total_activate_paind=total_activate_paid,current_paid=current_paid,
						unit_rate=float(unitRate['bonus_per_rate']),total_taka=total_taka,massage=message)
					if payment:
						# my_phone = MyDevice.objects.all()
						district = districtBangladesh.objects.all()
						my_phone.send_message({'messages': json_data}, collapse_key='something')
						context 	= 	{'panda':my_phone,
						'success': 'Payment Message Send Successfully','district':district,"navActive":"payment"}
						return render(request,'paymentSection/payment_gateway_template.html',context)
					
			else:
				my_phone = MyDevice.objects.filter(is_active=True)
				for my_phone in my_phone:
					userMy = MyUser.objects.only('id').get(id=my_phone.user.id)
					infoSalesActive 	= SaleInformation.objects.filter( Q(user__id=my_phone.user.id) & Q(activation__active_check=True) & Q(activation__check=True) ).values('activation__active_check').annotate(Active_count=Count('activation__active_check')).distinct()
					infoTotalpadding 	= SaleInformation.objects.filter( Q(user__id=my_phone.user.id) & Q(activation__check=True) & Q(activation__active_check=False) ).values('activation__check').annotate(Active_count=Count('activation__check')).distinct()

					payment = PaymentGatwayModel.objects.values('total_activate_paind').filter(salesUser=userMy).order_by('-id')

					if payment:
						total_activate_paid = int(payment[0]["total_activate_paind"])
					if infoTotalpadding:
						padding = int(infoTotalpadding[0]['Active_count'])
					if infoSalesActive:
						active  = int(infoSalesActive[0]['Active_count'])

					if active>total_activate_paid:
						current_paid = active - total_activate_paid
						total_activate_paid = current_paid + total_activate_paid
						total_taka = current_paid * float(unitRate['bonus_per_rate'])
					else:
						total_activate_paid = total_activate_paid
						current_paid = 0
						total_taka = current_paid * float(unitRate['bonus_per_rate'])

					payment = PaymentGatwayModel.objects.create(salesUser=userMy,
						total_activate_paind=total_activate_paid,current_paid=current_paid,
						unit_rate=float(unitRate['bonus_per_rate']),total_taka=total_taka,massage=message)

				MyDevice.objects.filter(is_active=True).send_message({'messages': json_data}, collapse_key='something')
				my_phone = MyDevice.objects.all()
				district = districtBangladesh.objects.all()
				context 	= 	{'panda':my_phone,'success': 'Payment Message Send Successfully','district':district,"navActive":"payment"}
				return render(request,'paymentSection/payment_gateway_template.html',context)
					

			my_phone = MyDevice.objects.all()
			district = districtBangladesh.objects.all()
			context 	= 	{'panda':my_phone,'success': 'Send Message Successfully','district':district,"navActive":"payment"}
			return render(request,'paymentSection/payment_gateway_template.html',context)
			

	else:
		district = districtBangladesh.objects.all()
		context = {'panda':my_phone,"district":district,"navActive":"payment"}
		return render(request,'paymentSection/payment_gateway_template.html',context)

def paymentList(request):

	if request.method == 'POST':
		search_text = request.POST['search_text']
		if search_text:
			payment = PaymentGatwayModel.objects.filter(Q(salesUser__username__contains=search_text) |
				Q(massage__contains=search_text) | Q(total_activate_paind__contains=search_text) |
				Q(current_paid__contains=search_text) | Q(total_taka__contains=search_text) |
				Q(unit_rate__contains=search_text) | Q(date__contains=search_text) ).order_by('-id')
			paginator = Paginator(payment, 20)
			page = request.GET.get('page')
			contacts = paginator.get_page(page)
			context = {'panda':contacts,"navActive":"payment"}
			return render(request,'paymentSection/payment_gateway_list_Search_template.html',context)
		else:
			payment = PaymentGatwayModel.objects.all().order_by('-id')
			paginator = Paginator(payment, 20)
			page = request.GET.get('page')
			contacts = paginator.get_page(page)
			context = {'panda':contacts,"navActive":"payment"}
			return render(request,'paymentSection/payment_gateway_list_Search_template.html',context)

	payment = PaymentGatwayModel.objects.all().order_by('-id')
	paginator = Paginator(payment, 20)
	page = request.GET.get('page')
	contacts = paginator.get_page(page)
	context = {'panda':contacts,"navActive":"payment"}
	return render(request,'paymentSection/payment_gateway_list_template.html',context)


def paymentListByID(request,id):

	if request.method == 'POST':
		search_text = request.POST['search_text']
		if search_text:
			payment = PaymentGatwayModel.objects.filter( Q(salesUser__id=id) & (Q(salesUser__username__contains=search_text) |
				Q(massage__contains=search_text) | Q(total_activate_paind__contains=search_text) |
				Q(current_paid__contains=search_text) | Q(total_taka__contains=search_text) |
				Q(unit_rate__contains=search_text) | Q(date__contains=search_text)) )
			paginator = Paginator(payment, 20)
			page = request.GET.get('page')
			contacts = paginator.get_page(page)
			context = {'panda':contacts,"id":id,"navActive":"createSales"}
			return render(request,'paymentSection/payment_gateway_list_Search_template.html',context)
		else:
			payment = PaymentGatwayModel.objects.filter(salesUser__id=id)
			paginator = Paginator(payment, 20)
			page = request.GET.get('page')
			contacts = paginator.get_page(page)
			context = {'panda':contacts,"id":id,"navActive":"createSales"}
			return render(request,'paymentSection/payment_gateway_list_Search_template.html',context)

	payment = PaymentGatwayModel.objects.filter(salesUser__id=id)
	paginator = Paginator(payment, 20)
	page = request.GET.get('page')
	contacts = paginator.get_page(page)
	context = {'panda':contacts,"id":id,"navActive":"createSales"}
	return render(request,'paymentSection/payment_gateway_list_by_id_template.html',context)


def paymentListDeleteByID(request,id):
	if request.user.is_admin:
		payment = PaymentGatwayModel.objects.filter(id=id)
		payment.delete()
		return redirect('paymentList')
	return redirect('paymentList')

def paymentListDelete(request):
	if request.user.is_admin:
		payment = PaymentGatwayModel.objects.all()
		payment.delete()
		return redirect('paymentList')
	return redirect('paymentList')