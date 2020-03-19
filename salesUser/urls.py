from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('create/',views.createSales,name='createSales'),
    path('list/',views.listOfSales,name='listOfSales'),
    path('salesInfo/',views.salesOfSales,name='salesOfSales'),
    path('editSaleProfile/<int:id>/',views.editSaleProfile,name='editSaleProfile'),
    path('password_reset/<int:id>/',views.password_reset,name='password_reset'),
    path('sales_info_for_user/<int:id>/',views.salesInfoForUser,name='salesInfoForUser'),
    # Delete
    path('delete_saleProfile/<int:id>/', views.delete_saleProfile, name='delete_saleProfile'),
    path('delete_saleInfo/<int:id>/', views.delete_saleInfo, name='delete_saleInfo'),
    path('delete_saleProfile_all/', views.delete_saleProfile_all, name='delete_saleProfile_all'),
    path('delete_salesInfo_all/', views.delete_salesInfo_all, name='delete_salesInfo_all'),
    # Search
    path('search_salesUser/', views.search_salesUser, name='search_salesUser'),
    path('search_saleInfo/', views.search_saleInfo, name='search_saleInfo'),
    # Export
    path('export_users_xl_sales/', views.export_users_xl_sales, name='export_users_xl_sales'),
    path('export_users_xl_salesInfo/', views.export_users_xl_salesInfo, name='export_users_xl_salesInfo'),
    


    # Password Reset URL
    # path('password_reset/',auth_views.password_reset,name='password_reset'),
    # path('password_reset/done/',auth_views.password_reset_done,name='password_reset_done'),
    # path('reset/<slug:uidb64>/<slug:token>)/', auth_views.password_reset_confirm, name='password_reset_confirm'),
    # path('reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),
    # path('',auth_views.password_reset,name='password_reset'),
    # path('password_reset/',auth_views.password_reset,name='password_reset'),


  

]