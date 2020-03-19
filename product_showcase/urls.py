from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib.auth.views import logout

urlpatterns = [
	path('product_type/', views.prodect_type, name='prodect_type'),
	path('product_speciality/', views.productSpeciality, name='productSpeciality'),
	path('productSpecialityDelete/', views.productSpecialityDelete, name='productSpecialityDelete'),
	path('productSpecialityDeleteByID/<int:id>/', views.productSpecialityDeleteByID, name='productSpecialityDeleteByID'),
	path('product_showcase/', views.productShowcase, name='productShowcase'),
	path('product_showcase_list/', views.product_list_show, name='product_list_show'),
	path('product_showcase_list_delete_by_id/<int:id>/', views.product_listDeleteByID, name='product_listDeleteByID'),
	path('product_showcase_list_delete_all/', views.product_listDeleteAll, name='product_listDeleteAll'),
]