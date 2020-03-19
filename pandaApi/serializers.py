from rest_framework import serializers
from rest_framework.authtoken.models import Token

from accounts.models import (SalesProfile,SaleInformation,
	MyUser,MyDevice,Message_Notification_Read,Message_Notification,
	BonusRate,TechnicalSupport,OfferPage,bankListBangladesh,offerType)

from product_showcase.models import Product_Type,Product_Speciality,Product_list
from deshbroad.models import activation_code
from paymentSection.models import PaymentGatwayModel

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db.models import Q

from fcm.utils import get_device_model


User = get_user_model()
Device = get_device_model()

import base64
from datetime import datetime
from dateutil.tz import tzlocal


from django.core.files.base import ContentFile



class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class SalesProfileEditImage(serializers.ModelSerializer):
	"""docstring for testserializer"""
	image 	  = Base64ImageField(max_length=None, use_url=True,allow_empty_file=True)
	class Meta:
		model = MyUser
		fields = [
		'image',
		]


class SalesProfileEditOne(serializers.ModelSerializer):
	"""docstring for testserializer"""
	full_name = serializers.CharField(allow_blank=True)
	email	  = serializers.EmailField(allow_blank=True)
	# image 	  = Base64ImageField(max_length=None, use_url=True,allow_empty_file=True)
	class Meta:
		model = MyUser
		fields = [
		'full_name',
		# 'image',
		'email',
		]

class salesSerializer(serializers.ModelSerializer):
	"""docstring for """
	company_address = serializers.CharField(allow_blank=True)
	phone_number 	= serializers.CharField(allow_blank=True)

	class Meta:
		model = SalesProfile
		fields = [
		'company_address',
		'phone_number',
		]
	


# test
class RegUserSerializer(serializers.ModelSerializer):

	user_details = salesSerializer()
	image 	  = Base64ImageField(required=False,max_length=None, allow_empty_file=True, use_url=True)
	# image		= serializers.ImageField(max_length=None,use_url=True,allow_empty_file=True)
	class Meta:
		model = MyUser
		fields = [
		'id',
		'full_name',
		'username',
		'password',
		'email',
		'image',
		'user_details',]
		# extra_kwargs = {'username':{'write_only':True},'email':{'write_only':True}}

	# def validate(self,data):
	# 	user_obj 		= None
	# 	username 		= data.get("username", None)
	# 	full_name 		= data.get("full_name", None)
	# 	email 			= data.get("email", None)
	# 	company_address = data['user_details']['company_address']
	# 	phone_number	= data['user_details']['phone_number']
	# 	# image 			= image_upload(data.FILES['image'],username)
	# 	# print(username)
	# 	password 	= data.get("password")

	# 	user = MyUser.objects.create(full_name=full_name,password=str(password),email=email,username=username,is_general_user=True)
	# 	user.save()
	# 	user = User.objects.get(username=username)
	# 	user.set_password(data.get("password"))
	# 	user.save()
	# 	# user_obj = user.first()
	# 	# user.set_password(password)
	# 	card = SalesProfile.objects.create(sales_user=user,company_address = company_address,
	# 	phone_number=phone_number)
	# 	if card:
	# 		return "1"
	# 	else:
			# return "0"

		

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

class SalesProfileSerializer(serializers.ModelSerializer):

	user_details = salesSerializer()
	# image			= serializers.ImageField(max_length=None,use_url=True)
	class Meta:
		model = MyUser
		fields = [
		'id',
		'full_name',
		'username',
		'email',
		'image',
		'user_details',]
		extra_kwargs = {'username':{'read_only':True},'email':{'read_only':True}}
		
			


class loginSerializer(serializers.ModelSerializer):
	"""docstring for ClassName"""
	token = serializers.CharField(allow_blank=True,read_only=True)
	username = serializers.CharField(required=True,write_only=True)
	class Meta:
		model = User
		fields = (
		
			'username',
			'password',
			'token',
			)
		extra_kwargs = {'password':{'write_only':True}}

	def validate(self,data):
		user_obj = None
		username = data.get("username", None)
		# print(username)
		password = data.get("password")
		nowLogin = datetime.now(tzlocal())
		print(nowLogin)
		if not username:
			raise ValidationError('Username Required To Login')

		user = User.objects.filter(Q(username=username) & Q(is_admin=False) & Q(is_staff=False) & Q(is_general_user=True)).distinct()


		# print(user[0])

		if user.exists() and user.count() == 1:
			user_obj = user.first()
			# print(user_obj)
			# for data in user:
			# 	print('dd')
		else:
			raise ValidationError('Username not validate')

		if user_obj:
			if not user_obj.check_password(password):
				raise ValidationError('Password not currect')
			updateIser = User.objects.filter(Q(username=username) & Q(is_admin=False) & Q(is_staff=False) & Q(is_general_user=True)).update(last_login=nowLogin)
		token, created = Token.objects.get_or_create(user_id=user_obj.id)
		# print(token.key)
		# data["email"] 	= user_obj.email
		data["token"] 	= token.key
		# data['id'] 		= user_obj.id

		return data

class checkActivationCodeSerializer(serializers.ModelSerializer):
	"""docstring for ClassName"""
	active_check = serializers.CharField(allow_blank=True,read_only=True)
	class Meta:
		model = activation_code
		fields = (
			'id',
			'file',
			'active_check',
			)
		extra_kwargs = {'file':{'write_only':True}}

	# def validate(self,data):
	# 	user_obj = None
	# 	sales_code = data.get("sales_code", None)
	# 	# print(username)
	# 	if not sales_code:
	# 		raise ValidationError('Qr Required To check')

	# 	activationCode = activation_code.objects.filter(Q(sales_code=sales_code) & Q(check=False)).distinct()
		
	# 	if activationCode.exists() and activationCode.count() == 1:
	# 		user_obj = activationCode.first()
	# 		# print(user_obj)
	# 	else:
	# 		data["check"] 	= "1"
	# 		return data;
	# 	data["check"] 	= "0"
	# 	data['id'] 		= user_obj.id

	# 	return data


class salesInfoSerializer(serializers.ModelSerializer):

	product__district_name = serializers.CharField(max_length=255,allow_blank=True,read_only=True)
	Active_point = serializers.CharField(max_length=255,allow_blank=True,read_only=True)
	class Meta:
		model = SaleInformation
		fields = (
			'activation',
			'user',
			'date',
			'product',
			'product__district_name',
			'Active_point',
			)
		extra_kwargs = {'user':{'read_only':True},
		'product__district_name':{'read_only':True},
		'Active_point':{'read_only':True},
		'activation':{'write_only':True},
		'product':{'write_only':True},}


class salesBonusSerializer(serializers.ModelSerializer):
	product_count = serializers.CharField(max_length=255,allow_blank=True)
	class Meta:
		model = SaleInformation
		fields = (
			'year',
			'month',
			'day',
			'product_count',
			)
		extra_kwargs = {'year':{'read_only':True},'month':{'read_only':True}
		,'day':{'read_only':True},'product_count':{'read_only':True},}


class salesPendingSerializer(serializers.ModelSerializer):
	# sales_count = serializers.CharField(max_length=255,allow_blank=True)
	Active_count = serializers.CharField(max_length=255,allow_blank=True)
	class Meta:
		model = SaleInformation
		fields = (
			'Active_count',
			)
		extra_kwargs = {'Active_count':{'read_only':True},}

class salesTotalSerializer(serializers.ModelSerializer):
	sales_count = serializers.CharField(max_length=255,allow_blank=True)
	# Active_count = serializers.CharField(max_length=255,allow_blank=True)
	class Meta:
		model = SaleInformation
		fields = (
			'sales_count',
			)
		extra_kwargs = {'sales_count':{'read_only':True},}



class FCMNotificationSerializer(serializers.ModelSerializer):
	dev_id = serializers.CharField(allow_blank=True,read_only=True)
	user = serializers.CharField(allow_blank=True,read_only=True)
	reg_id = serializers.CharField(required=False,allow_blank=True)
	class Meta:
		model = MyDevice
		fields = (
			'id',
			'dev_id',
			'reg_id',
			'name',
			'is_active',
			'user',
			)
		extra_kwargs = {'id':{'read_only':True},'name':{'read_only':True}}


class ChangePasswordSerializer(serializers.Serializer):
    
    old_password 	= serializers.CharField(required=True)
    new_password 	= serializers.CharField(required=True)
    retype_password = serializers.CharField(required=True)



# Notification
class MessageSerializer(serializers.Serializer):
	title = serializers.CharField(read_only=True,allow_blank=True,required=False)
	message = serializers.CharField(read_only=True,allow_blank=True,required=False)
	date = serializers.DateField(read_only=True)
	class Meta:
		model = Message_Notification
		fields = ('title','message','date',)

class MessageReadSerializer(serializers.Serializer):
	user_Message = serializers.CharField(read_only=True,allow_blank=True)
	message = MessageSerializer(required=False)
	read_flag = serializers.BooleanField()

	class Meta:
		model = Message_Notification_Read
		fields = (
			'user_Message',
			'message',
			'read_flag',
			)


# Bonus rate
class BonusRateSerializer(serializers.Serializer):
	bonus_per_rate = serializers.FloatField(default=0.0,read_only=True)
	class Meta:
		model = BonusRate
		fields = ('bonus_per_rate')

# Technical Support
class TechSupportSerializer(serializers.Serializer):
	phone_number = serializers.CharField(max_length=15,allow_blank=True,read_only=True)
	email 		 = serializers.EmailField(allow_blank=True,read_only=True)
	class Meta:
		model = TechnicalSupport
		fields = ('phone_number','email',)
		
			
# Offers
class Offers(serializers.Serializer):

	image_offer 	= serializers.ImageField(read_only=True)
	image_details 	= serializers.CharField(read_only=True)
	class Meta:
		model = OfferPage
		fields = ('image_offer','image_details')

# offer Type List
class OfferTypeList(serializers.Serializer):
	id 			= serializers.IntegerField(read_only=True)
	offer_name 	= serializers.CharField(read_only=True)
	class Meta:
		model = offerType
		fields = ('id','offer_name',)

class RewardSerializer(serializers.Serializer):
	user_Message = serializers.CharField(read_only=True,allow_blank=True)
	offers = Offers(required=False)
	read_flag = serializers.BooleanField()

	class Meta:
		model = Message_Notification_Read
		fields = (
			'user_Message',
			'offers',
			'read_flag',
			)

# Bank List
class BankList(serializers.Serializer):
	id 			= serializers.IntegerField(read_only=True)
	bank_name 	= serializers.CharField(read_only=True)
	class Meta:
		model = bankListBangladesh
		fields = ('id','bank_name',)
	


class ProductSpecialitySerializer(serializers.Serializer):
	id 							= serializers.IntegerField(read_only=True)
	product_speciality_name		= serializers.CharField(read_only=True)
	product_speciality_details 	= serializers.CharField(read_only=True)
	
	class Meta:
		model = Product_Speciality
		fields = ('id','product_speciality_name','product_speciality_details',)
		

class ProductListByProductID(serializers.Serializer):
	id 		= serializers.IntegerField(allow_null=True)
	name 	= serializers.CharField(read_only=True)
	details = serializers.CharField(read_only=True)
	product_type = serializers.CharField()
	product_speciality = ProductSpecialitySerializer(many=True,read_only=True)
	
	class Meta:
		model = Product_list
		fields = ('id','name','details','product_type','product_speciality')


class PaymentListSerializer(serializers.Serializer):
	massage 				= serializers.CharField(read_only=True)
	total_activate_paind 	= serializers.CharField(read_only=True)
	current_paid 			= serializers.CharField(read_only=True)
	unit_rate 				= serializers.CharField(read_only=True)
	total_taka 				= serializers.CharField(read_only=True)
	date 					= serializers.CharField(read_only=True)
	
	class Meta:
		model = PaymentGatwayModel
		fields = ('massage','total_activate_paind','current_paid','unit_rate','total_taka','date')
	
