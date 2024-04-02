from django import template
from women.models import *
from django.http import Http404


register = template.Library()

@register.simple_tag(name="getcats")
def get_categories():
    return Category.objects.all()

@register.inclusion_tag("women/list_categories.html")
def show_categories(sort=None, cat_selected='aktrisy'):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {"cats": cats, "cat_selected": cat_selected}



