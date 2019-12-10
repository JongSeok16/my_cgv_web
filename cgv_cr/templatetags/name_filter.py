from django import template

register = template.Library()

@register.filter
def get_item(dictionary):
    for i in dictionary.keys():
        return i

@register.filter
def get_items(dictionary):
    for e in dictionary.values():
        return e