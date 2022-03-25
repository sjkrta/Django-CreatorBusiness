from unicodedata import category
from django import template
register = template.Library()


def post_filter_by_category(Value, arg):
    return Value.filter(category__title=arg)

register.filter('post_filter_by_category', post_filter_by_category)