from django.urls import path
from . import views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),

    path('comparisons/', views.comparison_list, name='comparison_list'),
    path('comparisons/<slug:slug>/', views.comparison_detail, name='comparison_detail'),


    path('article/<slug:slug>/', views.article_detail, name='article_detail'),

    path('models/', views.models_list, name='models_list'),

    path('category/<str:category>/', views.category_articles, name='category_articles'),
    path('tag/<slug:slug>/', views.tag_list, name='tag_list'),

    path('privacy/', views.privacy, name='privacy'),
    path('agreement/', views.agreement, name='agreement'),

    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),


]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
