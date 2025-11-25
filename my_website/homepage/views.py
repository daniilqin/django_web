from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView, ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Collection
from .utils import HomeContextMixin

# Create your views here.

# categories_db = [
#     {'id': 'womens', 'name': 'Женщинам'},
#     {'id': 'mens', 'name': 'Мужчинам'},
#     {'id': 'kids', 'name': 'Детям'},
# ]


# Главная страница сайта
class IndexView(HomeContextMixin, ListView):
    model = Collection
    template_name = 'homepage/index.html'
    context_object_name = 'new_collections'
    page_title = 'Главная'
    
    def get_queryset(self):
        return Collection.published.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


# Страница акций и скидок
class PromotionsView(LoginRequiredMixin, HomeContextMixin, TemplateView):
    template_name = 'homepage/promotions.html'
    page_title = 'Акции и скидки'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


# Страница контактов
class ContactsView(HomeContextMixin, TemplateView):
    template_name = 'homepage/contacts.html'
    page_title = 'Контакты'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


# Страница "О сайте"
class AboutView(HomeContextMixin, TemplateView):
    template_name = 'homepage/about.html'
    page_title = 'О сайте'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


# Страница входа в систему
class LoginView(View):
    def get(self, request):
        return HttpResponse('<h1>Войти</h1>')


# def show_category(request, category_slug):
#     return HttpResponse(f'<h1>Категория - {category_slug}</h1>')


# Отображение конкретной коллекции
class CollectionView(LoginRequiredMixin, HomeContextMixin, DetailView):
    model = Collection
    template_name = 'homepage/collection.html'
    context_object_name = 'collection'
    slug_url_kwarg = 'collection_slug'
    
    def get_queryset(self):
        return Collection.published.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=self.object.title)
