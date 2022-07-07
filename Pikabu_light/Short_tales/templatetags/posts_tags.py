from django import template
from Short_tales.models import Posts, Category

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()