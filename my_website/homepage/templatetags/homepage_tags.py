from django import template 
# import homepage.views as views
from catalog.models import Category

register = template.Library()

TOP_CATEGORIES = {
    'Женщинам': 'zhenskaya-odezhda',
    'Мужчинам': 'muzhskaya-odezhda',
    'Детям': 'detskaya-odezhda',
}

# @register.simple_tag()
# def get_categories():
#     return views.categories_db

@register.simple_tag()
def get_top_categories():
    result = []
    for label, slug in TOP_CATEGORIES.items():
        try:
            cat = Category.objects.get(slug=slug)
            result.append({
                'name': label,             # Как отображается в меню
                'url': cat.get_absolute_url(),  # URL категории из БД
            })
        except Category.DoesNotExist:
            continue
    return result