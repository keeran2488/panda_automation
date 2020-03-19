from django.db import models
# from .models import bankListBangladesh

class activation_code(models.Model):
	"""docstring for activation_code"""
	file 			= models.CharField(max_length=255,unique=True)
	date 			= models.DateField(auto_now_add=True)
	product_type 	= models.ForeignKey("accounts.districtBangladesh",on_delete=models.SET_NULL,blank=True,null=True)
	active_check  	= models.BooleanField(default=False)
	active_date  	= models.CharField(max_length=200,blank=True)
	def __str__(self):
		return self.file

