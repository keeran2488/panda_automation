from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib.auth.views import logout

urlpatterns = [
	path('', views.index, name='index'),
	path('upload_code/', views.upload_activation, name='upload_activation'),
	path('upload_activate_code/', views.activate_code_upload, name='activate_code_upload'),

	path('list_of_activation/', views.list_of_activation, name='list_of_activation'),
	path('list_of_activation/activation_code_details/<str:date>/<str:product_type>/', views.activation_code_details, name='activation_code_details'),
	path('file_validation/', views.file_validation, name='file_validation'),
	path('file_validation_two/', views.file_validation_two, name='file_validation_two'),
	# Export
	path('export_users_xls/', views.export_users_xls,name='export_users_xls'),
	path('export_users_xls_batchCode/<str:date>/<str:product_type>/', views.export_users_xls_batchCode,name='export_users_xls_batchCode'),

	# Delete
	path('delete_all_activation_batch/', views.delete_all_activation_batch,name='delete_all_activation_batch'),
	path('delete_activation_batch/<str:date>/<str:product_type>/', views.delete_activation_batch,name='delete_activation_batch'),
	path('delete_activation_batchCode/<str:file>/<str:date>/<str:product_type>/', views.delete_activation_batchCode,name='delete_activation_batchCode'),

	#search
	path('search_activation/', views.search_activation,name='search_activation'),

	#Profile
	path('profile/', views.myProfile,name='myProfile'),
	path('password_reset_admin/', views.password_reset_admin,name='password_reset_admin'),

	#offer
	path('offers/', views.offersPage,name='offersPage'),
	path('offerlist/', views.offerList,name='offerList'),
	path('offers_type/', views.OfferType,name='OfferType'),
	path('delete_offers/<int:id>/', views.delete_offers,name='delete_offers'),
	path('delete_offers_all', views.delete_offers_all,name='delete_offers_all'),

    path('get-task-info/', views.get_task_info,name='get_task_info'),
    path('bonusRate/', views.bonusRate,name='bonusRate'),
    path('technicalSupport/', views.technicalSupport,name='technicalSupport'),

    # Excel file
    path('activation_excel/', views.excel_file,name='excel_file'),
]
