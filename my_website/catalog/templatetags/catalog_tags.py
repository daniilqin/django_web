from django import template 
import catalog.views as views

register = template.Library()


@register.inclusion_tag('catalog/includes/list_categories.html')
def show_categories():
    categories = views.categories_db
    return {'categories': categories}
