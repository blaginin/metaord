from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag
def namespaced_url(namespace, view_name, **kwargs):
    return reverse(namespace + ":" + view_name, kwargs=kwargs)
