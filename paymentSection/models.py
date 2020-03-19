import os
from django.conf import settings
from django.db import models
from accounts.models import SaleInformation,MyUser
from datetime import datetime

class PaymentGatwayModel(models.Model):
	salesUser 				= models.ForeignKey(MyUser, on_delete=models.CASCADE)
	total_activate_paind 	= models.IntegerField()
	current_paid 			= models.IntegerField()
	unit_rate 				= models.FloatField()
	total_taka 				= models.FloatField()
	massage 				= models.CharField(max_length=255,blank=True)
	date 					= models.DateField(default=datetime.now())

	def __str__(self):
		return str(self.massage)
	
		