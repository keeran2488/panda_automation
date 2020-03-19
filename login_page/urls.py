from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib.auth.views import logout

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('logout/', logout, {'next_page': settings.LOGIN_URL}, name='logout'),
]
