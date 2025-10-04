from django.urls import path, register_converter

from . import views, converters

register_converter(converters.DateConverter, 'ymd')

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('items/<slug:item_slug>/', views.item_detail, name='items'),
    path('events/<ymd:event_date>/', views.event_detail, name='events'),
    path('tag/<slug:tag_slug>/', views.show_tag, name='tag'),
    path('product/<slug:product_slug>/', views.show_product, name='product'),
    path('<slug:category_slug>/', views.show_category, name='category')
]
