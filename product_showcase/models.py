import os
from django.conf import settings
from django.db import models


class Product_Type(models.Model):
	product_type_name = models.CharField(max_length=100,blank=True)
	def __str__(self):
		return str(self.product_type_name)
	

class Product_Speciality(models.Model):
	product_speciality_name 	= models.CharField(max_length=255,blank=True,unique=True)
	product_speciality_details 	= models.CharField(max_length=255,blank=True)
	def __str__(self):
		return str(self.product_speciality_name)

# class Product_Showcase_details(models.Model):
# 	product_name 		= models.CharField(max_length=100,blank=True,unique=True)
# 	product_details 	= models.CharField(max_length=255,blank=True)
# 	product_type 		= models.ForeignKey(Product_Type, on_delete=models.CASCADE)
# 	product_speciality 	= models.ManyToManyField(Product_Speciality, related_name='product_speciality')
# 	def __str__(self):
# 		return str(self.product_name)

class Product_list(models.Model):
	name 				= models.CharField(max_length=100,blank=True,unique=True)
	details 			= models.CharField(max_length=255,blank=True)
	product_type 		= models.ForeignKey(Product_Type, on_delete=models.CASCADE)
	product_speciality 	= models.ManyToManyField(Product_Speciality, related_name='product_speciality')

	def __str__(self):
		return str(self.name)
		
		