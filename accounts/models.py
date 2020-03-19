import os
from django.conf import settings
from django.db import models
from deshbroad.models import activation_code
# Create your models here.
from django.core.validators import RegexValidator

from django.db.models.signals import post_delete
from django.dispatch import receiver

from django.contrib.auth.models import (
		BaseUserManager, AbstractBaseUser
	)

from fcm.models import AbstractDevice
from django import forms

USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'


class MyUserManager(BaseUserManager):
	def create_user(self, username, email, password=None):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
					username = username,
					email = self.normalize_email(email)
				)
		user.set_password(password)
		user.save(using=self._db)
		return user
		# user.password = password # bad - do not do this

	def create_superuser(self, username, email, password=None):
		user = self.create_user(
				username, email, password=password
			)

		user.is_admin 			= True
		user.is_staff 			= True
		user.is_general_user 	= True
		
		user.save(using=self._db)
		return user

def image_upload(instance,filename):
	filebase, extension = filename.split(".")
	return "%s/%s.%s"%(instance.username,instance.username,extension)


class MyUser(AbstractBaseUser):
	username = models.CharField(
					max_length=255,
					validators = [
						RegexValidator(regex = USERNAME_REGEX,
										message='Username must be alphanumeric or contain numbers',
										code='invalid_username'
							)],
					unique=True
				)
	email = models.EmailField(
			max_length=255,
			unique=True,
			verbose_name='email address'
		)
	full_name	 	= models.CharField(max_length=255, blank=True, null=True)
	image			= models.ImageField(upload_to=image_upload,blank=True,default='avatar.png')
	is_admin 		= models.BooleanField(default=False)
	is_staff 		= models.BooleanField(default=False)
	is_general_user = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.email

	def get_short_name(self):
		# The user is identified by their email address
		return self.username


	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True


	def delete(self, *args, **kwargs):
		self.image.delete()
		super(Picture, self).delete(*args, **kwargs)

	# def delete(self):
	# 	os.remove(settings.MEDIA_ROOT+''+self.instance.username+'/'+self.image.path)
	# 	return super(YourModel,self).delete()


class SalesProfile(models.Model):
	sales_user 		= models.OneToOneField(MyUser, on_delete=models.CASCADE,related_name="user_details")
	company_address = models.CharField(max_length=255,blank=True,null=True)
	# company_name	= models.CharField(max_length=255,blank=True,null=True)
	phone_number	= models.CharField(max_length=20,blank=True,null=True)
	# payment_account	= models.CharField(max_length=255,blank=True,null=True)
	# payment_method	= models.ForeignKey("bankListBangladesh",on_delete=models.SET_NULL,blank=True,null=True)
	# district_name	= models.ForeignKey("districtBangladesh",on_delete=models.SET_NULL,blank=True,null=True)

	def __str__(self):
		return str(self.sales_user)

class SaleInformation(models.Model):
	activation 	= 	models.OneToOneField(activation_code, on_delete=models.CASCADE)
	# activation	=	models.CharField(max_length=255,default='')
	user 		= 	models.ForeignKey(MyUser,on_delete=models.CASCADE)
	date		=	models.DateField(auto_now_add=True,blank=True)
	product		=	models.ForeignKey("districtBangladesh",on_delete=models.SET_NULL,blank=True,null=True)

	def __str__(self):
		return self.user

	

@receiver(post_delete, sender=MyUser)
def photo_post_delete_handler(sender, **kwargs):
	photo = kwargs['instance']

	storage, path = photo.image.storage, photo.image.path
	print("storage")
	storage.delete(path)
    # Pass false so FileField doesn't save the model.


    
	
class MyDevice(AbstractDevice):
	user = models.OneToOneField(MyUser,on_delete=models.CASCADE)


class Message_Notification(models.Model):
	title 	= models.CharField(max_length=100,blank=True)
	message = models.CharField(max_length=255,blank=True)
	date	= models.DateField(auto_now_add=True,blank=True)
	def __str__(self):
		return self.title


class Message_Notification_Read(models.Model):
	user_Message = models.ForeignKey(MyUser,on_delete=models.CASCADE,blank=True)
	message 	 = models.ForeignKey(Message_Notification,on_delete=models.CASCADE)
	read_flag	 = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user_Message)


class BonusRate(models.Model):
	bonus_per_rate = models.FloatField(default=0.0)

	def __str__(self):
		return str(self.bonus_per_rate)


class TechnicalSupport(models.Model):
	phone_number 	= models.CharField(max_length=15,blank=True)
	email 			= models.EmailField(blank=True)

	def __str__(self):
		return str(self.email)

# offers
class OfferPage(models.Model):
	# offer_name 		= models.ForeignKey("offerType",on_delete=models.SET_NULL,blank=True,null=True)
	image_offer 	= models.ImageField()
	image_details 	= models.TextField(blank=True)
	date	= models.DateField(auto_now_add=True,blank=True)

	def __str__(self):
		return str(self.id)

class Offer_Notification_Read(models.Model):
	user_Message = models.ForeignKey(MyUser,on_delete=models.CASCADE,blank=True)
	offers	 	 = models.ForeignKey(OfferPage,on_delete=models.CASCADE)
	read_flag	 = models.BooleanField(default=False)


class districtBangladesh(models.Model):
	district_name 	= models.CharField(max_length=25,blank=True,unique=True)
	product_point = models.FloatField(default=0.0)
	def __str__(self):
		return str(self.district_name)


class bankListBangladesh(models.Model):
	bank_name = models.CharField(max_length=50,blank=True,unique=True)
	def __str__(self):
		return str(self.bank_name)

# offers
class offerType(models.Model):
	offer_name = models.CharField(max_length=100,blank=True)
	def __str__(self):
		return str(self.offer_name)
	
		


@receiver(post_delete, sender=OfferPage)
def photo_post_delete_handler(sender, **kwargs):
	photo = kwargs['instance']
	storage, path = photo.image_offer.storage, photo.image_offer.path
	storage.delete(path)


