from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('create/',views.createAdmin,name='createAdmin'),
    path('list/',views.listAdmin,name='listAdmin'),
    # Delete
    path('deleteAdminAll/',views.deleteAdminAll,name='deleteAdminAll'),
    path('delete_Admin/<int:id>/', views.delete_Admin, name='delete_Admin'),

    # Export
    path('export_users_xl_UserAdmin/',views.export_users_xl_UserAdmin,name='export_users_xl_UserAdmin'),

    # messaging
    path('messaging/', views.messaging, name='messaging'),
    path('messagingList_for_all_user/', views.messagingList, name='messagingList'),
    path('messagingList/', views.messagingListTwo, name='messagingListTwo'),
    
    path('messagingListDelete/', views.messagingListDelete, name='messagingListDelete'),
    path('messagingListDeleteByID/<int:id>/', views.messagingListDeleteByID, name='messagingListDeleteByID'),
    
    path('messagingListTwoDelete/', views.messagingListTwoDelete, name='messagingListTwoDelete'),
    path('messagingListTwoDeleteByID/<int:id>/', views.messagingListTwoDeleteByID, name='messagingListTwoDeleteByID'),

    # Districts Of Bangladesh
    path('product/', views.districtsOFbangladesh, name='districtsOFbangladesh'),
    path('districtsOFbangladesh_DeleteAll/', views.districtsOFbangladesh_DeleteAll, name='districtsOFbangladesh_DeleteAll'),
    path('districtsOFbangladesh_DeleteByID/<int:id>/', views.districtsOFbangladesh_DeleteByID, name='districtsOFbangladesh_DeleteByID'),

    # Bank Of Bangladesh
    path('bank/', views.bankOFbangladesh, name='bankOFbangladesh'),
    path('bankOFbangladesh_DeleteAll/', views.bankOFbangladesh_DeleteAll, name='bankOFbangladesh_DeleteAll'),
    path('bankOFbangladesh_DeleteByID/<int:id>/', views.bankOFbangladesh_DeleteByID, name='bankOFbangladesh_DeleteByID'),

]