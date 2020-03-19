from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib.auth.views import logout

urlpatterns = [
	path('payment_gateway/', views.paymentGateway, name='paymentGateway'),
	path('payment_list/', views.paymentList, name='paymentList'),
	path('payment_list_by_user/<int:id>/', views.paymentListByID, name='paymentListByID'),
	path('paymentListDelete/', views.paymentListDelete, name='paymentListDelete'),
	path('paymentListDeleteByID/<int:id>', views.paymentListDeleteByID, name='paymentListDeleteByID'),
]