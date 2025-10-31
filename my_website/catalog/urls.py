from django.urls import path, register_converter

from . import views, converters

register_converter(converters.DateConverter, 'ymd')

urlpatterns = [
    path('', views.CatalogView.as_view(), name='catalog'),
    path('add_product/', views.AddProductView.as_view(), name='add_product'),
    path('upload_file/', views.UploadFileView.as_view(), name='upload_file'),
    path('items/<slug:item_slug>/', views.item_detail, name='items'),
    path('events/<ymd:event_date>/', views.event_detail, name='events'),
    path('tag/<slug:tag_slug>/', views.TagView.as_view(), name='tag'),
    path('product/<slug:product_slug>/', views.ProductView.as_view(), name='product'),
    path('product/<slug:product_slug>/edit/', views.UpdateProductView.as_view(), name='edit_product'),
    path('product/<slug:product_slug>/delete/', views.DeleteProductView.as_view(), name='delete_product'),
    path('<slug:category_slug>/', views.CategoryView.as_view(), name='category'),
]
