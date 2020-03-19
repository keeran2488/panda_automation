import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse

from django.db.models import Count,Sum
from django.db.models import Q
from django.core.exceptions import ValidationError

from accounts.models import (
	SalesProfile,
	SaleInformation,
	MyUser,MyDevice,
	Message_Notification_Read,
	Message_Notification,
	BonusRate,
	TechnicalSupport,
	OfferPage,
	bankListBangladesh,
	districtBangladesh,
	offerType,
	Offer_Notification_Read,
	)

from paymentSection.models import PaymentGatwayModel
from product_showcase.models import Product_Type,Product_Speciality,Product_list

from deshbroad.models import activation_code

from .serializers import (
	SalesProfileSerializer,
	loginSerializer,
	checkActivationCodeSerializer,
	salesInfoSerializer,
	SalesProfileEditOne,
	salesSerializer,
	SalesProfileEditImage,
	ChangePasswordSerializer,
	FCMNotificationSerializer,
	MessageReadSerializer,
	salesBonusSerializer,
	salesPendingSerializer,
	salesTotalSerializer,
	BonusRateSerializer,
	TechSupportSerializer,
	Offers,
	BankList,
	OfferTypeList,
	ProductListByProductID,
	ProductSpecialitySerializer,
	PaymentListSerializer,
	RegUserSerializer,
	RewardSerializer,
	)

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FileUploadParser
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

import datetime

from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	)

from fcm.utils import get_device_model
Device = get_device_model()

from accounts.code import codeKey,chekDatafram,dataWrap
key = codeKey()
dataframe = chekDatafram(key)

class EditProfileOne(generics.RetrieveUpdateDestroyAPIView):
	lookup_field		= 'pk'
	permission_classes = [IsAuthenticated]
	authentication_classes = (TokenAuthentication,)
	serializer_class = SalesProfileEditOne
	# queryset = MyUser.objects.all()
	parser_classes = (MultiPartParser,)

	def get_queryset(self):
		return MyUser.objects.all()

	def update(self,request,pk=None):
		serializer = SalesProfileEditOne(data=request.data)
		if serializer.is_valid():
			print("ok")
			full_name 			= serializer.data.get('full_name')
			email 				= serializer.data.get('email')
			qry = MyUser.objects.filter(pk=self.request.user.id).update(full_name=full_name,email=email)

			if qry==1:
				return Response(qry,status=status.HTTP_200_OK)
			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
		print(serializer)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


	# def post(self,request):
	# 	serializer = testserializer(data=request.data)

	# 	if serializer.is_valid():
	# 		name = serializer.data.get('full_name')
	# 		message = 'Hello {0}'.format(name)
	# 		return Response({'message':message})
	# 	else:
	# 		return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)

class EditProfileTwo(generics.RetrieveUpdateDestroyAPIView):
	# lookup_field		= 'user'
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	serializer_class = salesSerializer
	# queryset 	= SalesProfile.objects.all()
	def get_queryset(self):
		return SalesProfile.objects.filter(sales_user=self.request.user.id)

	def update(self, request, pk=None):
		
		serializer = salesSerializer(data=request.data)

		if serializer.is_valid():

			company_address 	= serializer.data.get('company_address')
			phone_number 		= serializer.data.get('phone_number')
			# payment_account 	= serializer.data.get('payment_account')
			# payment_method 		= serializer.data.get('payment_method')
			# district_name 		= serializer.data.get('district_name')

			qry = SalesProfile.objects.filter(sales_user=self.request.user.id).update(company_address=company_address,
				phone_number=phone_number)
			if qry==1:
				return Response(qry,status=status.HTTP_200_OK)
			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

			# return Response(full_name,status=status.HTTP_400_BAD_REQUEST)
			
		else:
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class EditProfileImage(generics.RetrieveUpdateDestroyAPIView):
	lookup_field		= 'pk'
	permission_classes = [IsAuthenticated]
	authentication_classes = (TokenAuthentication,)
	serializer_class = SalesProfileEditImage
	# queryset = MyUser.objects.all()
	def get_queryset(self):
		return MyUser.objects.all()

	def update(self, request, pk=None):
		
		serializer = SalesProfileEditImage(data=request.FILES)
		if serializer.is_valid():
			
			image = request.FILES['image']
			# print(image)
			if image is not None:
				image = image_upload(image,self.request.user.username)
				print("image")
				qry = MyUser.objects.filter(pk=self.request.user.id).update(image=image)

				if qry==1:
					return Response(qry,status=status.HTTP_200_OK)
				else:
					return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
			else:
				print('null')
			# return Response(full_name,status=status.HTTP_400_BAD_REQUEST)
			
		else:
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class loginview(APIView):
	"""docstring for ClassName"""
	permission_classes = [AllowAny]
	serializer_class = loginSerializer
	def post(self,request,*args,**kwargs):
		data = request.data
		serializer = loginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data = serializer.data
			# print(serializer.data)
			return Response(new_data,status=status.HTTP_200_OK)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class RegView(APIView):
	"""docstring for ClassName"""
	permission_classes = [AllowAny]
	serializer_class = RegUserSerializer
	def post(self,request,*args,**kwargs):
		# obj = self.get_object()
		data = request.data
		serializer = RegUserSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data 		= serializer.data
			username 		= serializer.data.get("username", None)
			full_name 		= serializer.data.get("full_name")
			email 			= serializer.data.get("email")
			company_address = serializer.data['user_details']['company_address']
			phone_number	= serializer.data['user_details']['phone_number']
			password 		= serializer.data.get("password")

			image = request.FILES.get('image',None)

			if image is not None:
				# return Response({"data":"1"},status=status.HTTP_200_OK)
				image = image_upload(image,username)
				user = MyUser.objects.create(image=image,full_name=full_name,password=password,email=email,username=username,is_general_user=True)
				user.save()
				user = MyUser.objects.get(username=username)
				dataUser = SalesProfile.objects.create(sales_user=user,company_address = company_address,phone_number=phone_number)
				user.set_password(password)
				user.save()
				if dataUser:
					return Response(new_data,status=status.HTTP_200_OK)
				else:
					return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
			else:
				user = MyUser.objects.create(full_name=full_name,password=password,email=email,username=username,is_general_user=True)
				user.save()
				user = MyUser.objects.get(username=username)
				dataUser = SalesProfile.objects.create(sales_user=user,company_address = company_address,phone_number=phone_number)
				user.set_password(password)
				user.save()
				if dataUser:
					return Response(new_data,status=status.HTTP_200_OK)
				else:
					return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
			# print(serializer.data)
			return Response({"data":"1"},status=status.HTTP_200_OK)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# class chechActivation(APIView):
# 	"""docstring for ClassName"""
# 	permission_classes = [IsAuthenticated]
# 	authentication_classes = (TokenAuthentication,)
# 	serializer_class = checkActivationCodeSerializer
# 	def post(self,request,*args,**kwargs):
# 		data = request.data
# 		# print(self.request.user)
# 		serializer = checkActivationCodeSerializer(data=data)
# 		if serializer.is_valid(raise_exception=True):
# 			new_data = serializer.data
# 			# print(serializer.data)
# 			return Response(new_data,status=status.HTTP_200_OK)
# 		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class checkActivation(viewsets.ModelViewSet):
	"""docstring for """
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	serializer_class = checkActivationCodeSerializer
	# queryset 	= SaleInformation.objects.all()

	def get_queryset(self):
		return activation_code.objects.filter(active_check=True)

	def create(self,serializer):
		file = self.request.data['file']
		checkData = dataframe[dataframe['file2'] == file]
		if checkData.empty:
			file = self.request.data['file']
		else:
			file = checkData['file'].values[0]

		activationCode = activation_code.objects.filter(Q(file=file) & Q(active_check=False)).distinct()
		if activationCode.exists() and activationCode.count() == 1:
			user_obj = activationCode.first()
			return Response({"check":activationCode.count(),"id":user_obj.id,"product":user_obj.product_type.id},status=status.HTTP_200_OK)
		else:
			return Response({"check":activationCode.count()},status=status.HTTP_200_OK)
		return Response({"check":""},status=status.HTTP_400_BAD_REQUEST)

class salesInformation(viewsets.ModelViewSet):
	"""docstring for """
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	serializer_class = salesInfoSerializer
	# queryset 	= SaleInformation.objects.all()

	def get_queryset(self):
		return SaleInformation.objects.filter( Q(user__id=self.request.user.id) & Q(activation__active_check=True) ).values('product__district_name').annotate(Active_point=Sum('product__product_point'))

	def perform_create(self,serializer):
		data = activation_code.objects.filter(id=self.request.data['activation']).update(active_check=True)
		product = districtBangladesh.objects.only('id').get(id=self.request.data['product'])
		now = datetime.date.today()
		serializer.save(user=self.request.user,product=product)

class salesInformationBonus(viewsets.ModelViewSet):
	"""docstring for """
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	serializer_class = salesBonusSerializer

	def get_queryset(self):
		return SaleInformation.objects.filter(user=self.request.user).values('year','month').annotate(product_count=Count('month')).distinct().order_by("-year")

class salesInformationPending(viewsets.ModelViewSet):
	"""docstring for """
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	serializer_class = salesPendingSerializer

	def get_queryset(self):
		info = SaleInformation.objects.filter( Q(user=self.request.user) & Q(activation__active_check=True) & Q(activation__check=True) ).values('activation__active_check').annotate(Active_count=Count('activation__active_check')).distinct()
		return info

class salesInformationTotal(viewsets.ModelViewSet):
	"""docstring for """
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	serializer_class = salesTotalSerializer

	def get_queryset(self):
		info = SaleInformation.objects.filter(Q(user=self.request.user) & Q(activation__check=True)).values('activation__check').annotate(sales_count=Count('activation__check')).distinct()
		return info



class userProfile(viewsets.ModelViewSet):
	"""docstring for """
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	serializer_class = SalesProfileSerializer
	# queryset 	= SaleInformation.objects.all()
	parser_classes = (MultiPartParser,)

	def get_queryset(self):
		return MyUser.objects.select_related('user_details').filter(pk=self.request.user.id)

	def update(self, request, pk=None):
		
		serializer = SalesProfileSerializer(data=request.data)
		if serializer.is_valid():

			full_name 			= serializer.data.get('full_name')
			# username 			= serializer.data.get('username')
			image				= request.FILES['image']
			company_address 	= serializer.data['user_details']['company_address']
			company_name 		= serializer.data['user_details']['company_name']
			phone_number 		= serializer.data['user_details']['phone_number']
			payment_account 	= serializer.data['user_details']['payment_account']

			if image is not None:
				image = image_upload(image,self.request.user.id)
				print(image)
				qry = MyUser.objects.filter(pk=self.request.user.id).update(full_name=full_name,image=image)
			else:
				qry = MyUser.objects.filter(pk=self.request.user.id).update(full_name=full_name,)

			# qry = MyUser.objects.filter(pk=self.request.user.id).update(full_name=full_name,)
			qry2 = SalesProfile.objects.filter(sales_user=self.request.user.id).update(company_address=company_address,
				company_name=company_name,phone_number=phone_number,payment_account=payment_account)

			if qry==1 & qry2==1:
				return Response(serializer.data,status=status.HTTP_200_OK)
			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
			# return Response(full_name,status=status.HTTP_400_BAD_REQUEST)
			
		else:
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


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
	

# Password change
class ChangePasswordView(generics.UpdateAPIView):
	serializer_class = ChangePasswordSerializer
	model = MyUser
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)

	def get_object(self, queryset=None):
		obj = self.request.user
		return obj

	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			new_pass 	= serializer.data.get("new_password")
			retype_pass = serializer.data.get("retype_password")
			# Check old password
			if not self.object.check_password(serializer.data.get("old_password")):
				return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

			# Check old retype_pass
			if new_pass  == retype_pass:
				self.object.set_password(serializer.data.get("new_password"))
				self.object.save()
				return Response("Success.", status=status.HTTP_200_OK)
			else:
				return Response({"retype_password": ["Retype Password does not match"]}, status=status.HTTP_400_BAD_REQUEST)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# FCM

class notificationFCM(viewsets.ModelViewSet):
	"""docstring for """
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	serializer_class = FCMNotificationSerializer
	# queryset 	= SaleInformation.objects.all()

	def get_queryset(self):
		return MyDevice.objects.filter(user=self.request.user.id)

	def perform_create(self,serializer):
		serializer.save(user=self.request.user,name=self.request.user.username,dev_id=self.request.user)

	def update(self, request, pk=None):
		serializer = FCMNotificationSerializer(data=request.data)
		if serializer.is_valid():
			reg_id = serializer.data.get('reg_id')
			is_active = serializer.data.get('is_active')
			if reg_id:
				qry = MyDevice.objects.filter(user=self.request.user.id).update(reg_id=reg_id)
			else:
				qry = MyDevice.objects.filter(user=self.request.user.id).update(is_active=is_active)

			if qry==1:
				return Response(qry,status=status.HTTP_200_OK)
			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# Notification Section

class notificationMessage(viewsets.ModelViewSet):
	"""docstring for """
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	serializer_class = MessageReadSerializer
	# queryset 	= SaleInformation.objects.all()

	def get_queryset(self):
		return Message_Notification_Read.objects.select_related('message').filter(user_Message=self.request.user)
	def create(self,serializer):
		qry = Message_Notification_Read.objects.filter(user_Message=self.request.user).update(read_flag=True)
		if qry:
			return Response(qry,status=status.HTTP_200_OK)
		else:
			return Response(qry,status=status.HTTP_400_BAD_REQUEST)


class Reward(viewsets.ModelViewSet):
	"""docstring for """
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	serializer_class = RewardSerializer
	# queryset 	= SaleInformation.objects.all()

	def get_queryset(self):
		return Offer_Notification_Read.objects.select_related('offers').filter(user_Message=self.request.user)
	def create(self,serializer):
		qry = Offer_Notification_Read.objects.filter(user_Message=self.request.user).update(read_flag=True)
		if qry:
			return Response(qry,status=status.HTTP_200_OK)
		else:
			return Response(qry,status=status.HTTP_400_BAD_REQUEST)


# Bonus Rate
class bonusRate(viewsets.ModelViewSet):
	"""docstring for """
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	serializer_class = BonusRateSerializer
	# queryset 	= SaleInformation.objects.all()

	def get_queryset(self):
		return BonusRate.objects.all()


# Technical Support
class TechnSupport(viewsets.ModelViewSet):
	"""docstring for """
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	serializer_class = TechSupportSerializer
	# queryset 	= SaleInformation.objects.all()

	def get_queryset(self):
		return TechnicalSupport.objects.all()

# Offers
# class OffersPage(viewsets.ModelViewSet):
# 	"""docstring for """
# 	authentication_classes = (TokenAuthentication,)
# 	permission_classes = [IsAuthenticated]
# 	serializer_class = Offers
# 	# queryset 	= SaleInformation.objects.all()

# 	def get_queryset(self):
# 		return OfferPage.objects.all()

class OffersPage(APIView):
	# lookup_field		= 'user'
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	serializer_class = Offers
	
	def post(self, request, format=None):
		serializer = Offers(data=request.data)
		if serializer.is_valid():
			data = OfferPage.objects.all()
			serializer = Offers(data, many=True)
			return Response(serializer.data)
		return Response({'Post':'Post'})



# Offers list
class OffersList(viewsets.ModelViewSet):
	"""docstring for """
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	serializer_class = Offers

	def get_queryset(self):
		return OfferPage.objects.all()

# Bank list
class BankName(viewsets.ModelViewSet):
	"""docstring for """
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	serializer_class = BankList

	def get_queryset(self):
		return bankListBangladesh.objects.all()

# Product Speciality
class ProductSpeciality(viewsets.ModelViewSet):
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	serializer_class = ProductSpecialitySerializer

	def get_queryset(self):
		return Product_Speciality.objects.all()


class ProductListByID(APIView):
	# lookup_field		= 'user'
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	serializer_class = ProductListByProductID
	
	def post(self, request, format=None):
		serializer = ProductListByProductID(data=request.data)
		if serializer.is_valid():
			if int(request.data['id']) > -1:
				data = Product_list.objects.filter(id=request.data['id'],product_type=request.data['product_type'])
			else:
				data = Product_list.objects.filter(product_type=request.data['product_type'])
			serializer = ProductListByProductID(data, many=True)
			return Response(serializer.data)
		return Response({'Post':'Post'})

# Payment
class PaymentList(viewsets.ModelViewSet):

	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	serializer_class = PaymentListSerializer
	# queryset 	= SaleInformation.objects.all()
	parser_classes = (MultiPartParser,)

	def get_queryset(self):
		return PaymentGatwayModel.objects.filter(salesUser=self.request.user.id).order_by('-id')
