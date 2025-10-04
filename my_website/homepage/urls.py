from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('promotions/', views.promotions, name='promotions'),
    path('contacts/', views.contacts, name='contacts'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
#     path('category/<slug:category_slug>/', views.show_category,
#          name='category'),
    path('collection/<slug:collection_slug>', views.show_collection,
         name='collection')
]
