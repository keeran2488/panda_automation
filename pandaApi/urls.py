from django.contrib import admin
from django.urls import path, include
from pandaApi.views import (
	EditProfileOne,
	loginview,
	checkActivation,
	salesInformation,
	userProfile,
	EditProfileTwo,
	EditProfileImage,
	ChangePasswordView,
	notificationFCM,
	notificationMessage,
	salesInformationBonus,
	salesInformationPending,
	salesInformationTotal,
	bonusRate,
	TechnSupport,
	OffersPage,
	BankName,
	OffersList,
	ProductListByID,
	ProductSpeciality,
	PaymentList,
	RegView,
	Reward,

	)

from django.conf import settings

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('salesInformation',salesInformation,base_name='salesInformation')
router.register('checkActivation',checkActivation,base_name='checkActivation')
router.register('userProfile',userProfile,base_name='userProfile')
router.register('notificationFCM',notificationFCM,base_name='notificationFCM')
router.register('notificationMessage',notificationMessage,base_name='notificationMessage')
router.register('salesInformationBonus',salesInformationBonus,base_name='salesInformationBonus')
router.register('salesInformationPending',salesInformationPending,base_name='salesInformationPending')
router.register('salesInformationTotal',salesInformationTotal,base_name='salesInformationTotal')
router.register('bonusRate',bonusRate,base_name='bonusRate')
router.register('TechnSupport',TechnSupport,base_name='TechnSupport')
# router.register('OffersPage',OffersPage,base_name='OffersPage')
router.register('BankName',BankName,base_name='BankName')
router.register('OffersList',OffersList,base_name='OffersList')
router.register('ProductSpeciality',ProductSpeciality,base_name='ProductSpeciality')
router.register('PaymentList',PaymentList,base_name='PaymentList')
router.register('Reward',Reward,base_name='Reward')

urlpatterns = [
	path('loginAPI/', loginview.as_view(), name='loginview'),
	path('regAPI/', RegView.as_view(), name='RegView'),
	# path('checkActivation/', chechActivation.as_view(), name='chechActivation'),
	path('EditProfileOne/<int:pk>/', EditProfileOne.as_view(), name='post-rud'),
	path('EditProfileTwo/<int:pk>/', EditProfileTwo.as_view(), name='post-rud'),
	path('EditProfileImage/<int:pk>/', EditProfileImage.as_view(), name='post-rud'),
	path('ChangePasswordView/', ChangePasswordView.as_view(), name='post-rud'),

	path('OffersPage/', OffersPage.as_view(), name='post-rud'),
	path('ProductListByID/', ProductListByID.as_view(), name='post-rud'),
	
	path('',include(router.urls)),

]
