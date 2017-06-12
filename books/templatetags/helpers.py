# -*- coding: utf-8 -*-
from django import template
register = template.Library()

@register.filter()
def bettertitle(value):
    """
    Alternative to the builtin title(); uppercases words without replacing letters that are already uppercase.
    """
    return ' '.join([w[0].upper() + w[1:] for w in value.split()])

@register.filter()
def example_choices(value, arg=3):
    choices = []
    for id, label in value:
        if len(choices) == arg:
            choices.append('etc.')
            break
        if not id:
            continue
        choices.append(label)
    return ', '.join(choices) or 'None'

@register.simple_tag()
def querystring(request, **kwargs):
    """
    Append or update the page number in a querystring.
    """
    querydict = request.GET.copy()
    for k, v in kwargs.items():
        if v is not None:
            querydict[k] = v
        elif k in querydict:
            querydict.pop(k)
    querystring = querydict.urlencode()
    if querystring:
        return '?' + querystring
    else:
        return ''
