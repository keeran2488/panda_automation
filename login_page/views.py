from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.views.generic import CreateView
from django.contrib.auth.forms import (UserCreationForm,PasswordChangeForm)
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model

from django.db.models import Q


from django.core import validators
from django.core.exceptions import ValidationError

User = get_user_model()


def login_view(request):
	error =""
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['key']
		
		user = authenticate(request, username=username, password=password)
		if user is not None:
			if user.is_active and (user.is_general_user==False or user.is_staff or user.is_admin):
				login(request, user)
				return redirect('index')	
			else:
				error = "Invalid User"
				context = {"error":error}
				return render(request, 'login/login.html',context)	
		else:
			error = "Invalid Username OR Password"
			context = {"error":error}
			return render(request, 'login/login.html',context)
	else:
		if not request.user.is_authenticated:
			context = {"error":error}
			return render(request, 'login/login.html',context)
		else:
			return redirect('index')



