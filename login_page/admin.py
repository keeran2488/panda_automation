from django.contrib import admin

from deshbroad.models import activation_code
from accounts.models import MyDevice
# Register your models here.
admin.site.register(activation_code)
admin.site.register(MyDevice)