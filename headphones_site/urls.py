"""
URL configuration for headphones_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import user_passes_test
from ckeditor_uploader import views as ck_views

# Доступ к загрузке через CKEditor — только для staff
staff_required = user_passes_test(lambda u: u.is_active and u.is_staff)



urlpatterns = [
    path('admin/', admin.site.urls),
# CKEditor (загрузка/обзор файлов): закрыто для staff
    path('ckeditor/upload/', staff_required(ck_views.upload), name='ckeditor_upload'),
    path('ckeditor/browse/', staff_required(ck_views.browse), name='ckeditor_browse'),

    # Публичные маршруты вашего приложения
    path('', include('content.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


