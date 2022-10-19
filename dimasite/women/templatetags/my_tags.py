from django import template
from women.models import *
from women.views import menu

register = template.Library()


@register.simple_tag()
def get_menu(param):
    my_menu=menu.copy()
    if param:
        return menu
    my_menu.pop(1)
    return my_menu

@register.inclusion_tag("women/list_categories.html")
def show_categories(cat_selected):
    cat_list = Category.objects.all()
    return {"cats": cat_list, "cat_selected": cat_selected}
