# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django import template

register = template.Library()


@register.filter(name='addclass')
def addclass(value, extra_classes):
    classes = value.css_classes(extra_classes)
    return value.as_widget(attrs={'class': classes})


@register.filter('has_group')
def has_group(user, group_name):
    groups = user.groups.all()
    if not groups:
        return False
    group_names = groups.values_list('name', flat=True)
    return True if group_name in group_names else False

@register.filter(name="lookup")
def lookup(dictionary, key):
    return dictionary.get(key, "")
