from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from import_export.admin import ImportExportModelAdmin

# from .forms import UserCreationForm
from .models import (
	MyUser,
	SalesProfile,
	SaleInformation,
	Message_Notification,
	Message_Notification_Read,
	BonusRate,
	TechnicalSupport,
	OfferPage,
	districtBangladesh,
	bankListBangladesh,
	offerType,
	Offer_Notification_Read,
)



# Register your models here.

class UserAdmin(BaseUserAdmin):
	# add_form = UserCreationForm

	list_display = ('username','email','is_admin','is_staff','is_general_user')
	list_filter = ('is_admin',)

	fieldsets = (
			(None, {'fields': ('username','full_name','email','password','image')}),
			('Permissions', {'fields': ('is_admin','is_staff','is_general_user')})
		)
	search_fields = ('username','email')
	ordering = ('username','email')

	filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)
admin.site.register(SalesProfile)
admin.site.register(SaleInformation)

admin.site.register(Message_Notification)
admin.site.register(Message_Notification_Read)
admin.site.register(BonusRate)
admin.site.register(TechnicalSupport)
admin.site.register(OfferPage)
admin.site.register(districtBangladesh)
admin.site.register(bankListBangladesh)
admin.site.register(offerType)
admin.site.register(Offer_Notification_Read)

admin.site.unregister(Group)