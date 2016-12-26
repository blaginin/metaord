from django.template import Template, Context
from metaord import settings
import requests
import json
import urllib


def order_upd_status(order):
    if order.project.pb_order_upd_status and order.project.pb_url:
        tmpl = Template(order.project.pb_order_upd_status)
        ctx = Context({"order": order})
        if settings.DEBUG: print("Postback order_upd_status msg: `{0}`".format(tmpl.render(ctx)))
        h = {"Content-type": "application/x-www-form-urlencoded"}
        p = [(k, v) for k, v in json.loads(tmpl.render(ctx)).items()]
        r = requests.get(order.project.pb_url, params=p, headers=h)

def order_created(order):
    if order.project.pb_order_upd_status and order.project.pb_url:
        tmpl = Template(order.project.pb_order_create)
        ctx = Context({"order": order})
        if settings.DEBUG: print("Postback order_created msg: `{0}`".format(tmpl.render(ctx)))
        h = {"Content-type": "application/x-www-form-urlencoded"}
        p = [(k, v) for k, v in json.loads(tmpl.render(ctx)).items()]
        r = requests.get(order.project.pb_url, params=p, headers=h)
