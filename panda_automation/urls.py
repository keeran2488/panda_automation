from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import (handler400, handler403, handler404, handler500)
handler400 = 'deshbroad.views.bad_request'
handler403 = 'deshbroad.views.bad_request'
handler404 = 'deshbroad.views.bad_request'
handler500 = 'deshbroad.views.bad_request'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('login_page.urls')),
    path('', include('deshbroad.urls')),
    path('salesUser/', include('salesUser.urls')),
    path('mendim_api/', include('pandaApi.urls')),
    path('administration/', include('administrationSection.urls')),
    path('product_showcase/', include('product_showcase.urls')),
    path('payment/', include('paymentSection.urls')),

]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)