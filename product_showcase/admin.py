from django.contrib import admin

# Register your models here.
from product_showcase.models import Product_Type,Product_Speciality,Product_list

admin.site.register(Product_Type)
admin.site.register(Product_Speciality)
admin.site.register(Product_list)