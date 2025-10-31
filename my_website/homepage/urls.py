from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='homepage'),
    path('promotions/', views.PromotionsView.as_view(), name='promotions'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('login/', views.LoginView.as_view(), name='login'),
#     path('category/<slug:category_slug>/', views.show_category,
#          name='category'),
    path('collection/<slug:collection_slug>', views.CollectionView.as_view(), name='collection')
]
