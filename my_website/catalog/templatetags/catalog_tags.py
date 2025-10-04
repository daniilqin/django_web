from django import template 
from django.db.models import Count
from catalog.models import Category, Tag

register = template.Library()


@register.inclusion_tag('catalog/includes/list_categories.html')
def show_categories():
    categories = Category.objects.all()
    # categories = Category.objects.annotate(total=Count("products")).filter(total__gt=0)
    return {'categories': categories}


@register.inclusion_tag('catalog/includes/list_tags.html')
def show_tags():
    tags = Tag.objects.all()
    # tags = Tag.objects.annotate(total=Count("products")).filter(total__gt=0)
    return {'tags': tags}
