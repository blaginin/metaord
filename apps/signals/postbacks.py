from django.template import Template, Context
from metaord import settings
import requests
import json
import urllib

def process_order(order):
    data = order.__dict__.copy()

    copy = ['post_date', 'project', 'id']
    
    for i in copy:
        data[i] = order.__getattribute__(i)

    data['post_date'] = int(data['post_date'].timestamp()//1)

    return data

def order_upd_status(order):
    if order.project.pb_order_upd_status and order.project.pb_url:
        context_order = process_order(order)
        tmpl = Template(order.project.pb_order_upd_status)
        ctx = Context({"order": context_order})

        if settings.DEBUG: print("Postback order_upd_status msg: `{0}`".format(tmpl.render(ctx)))
        h = {"Content-type": "application/x-www-form-urlencoded"}
        p = [(k, v) for k, v in json.loads(tmpl.render(ctx)).items()]
        r = requests.post(order.project.pb_url, data=p, headers=h)

def order_created(order):
    if order.project.pb_order_upd_status and order.project.pb_url:
        context_order = process_order(order)
        tmpl = Template(order.project.pb_order_create)
        ctx = Context({"order": context_order})
        if settings.DEBUG: print("Postback order_created msg: `{0}`".format(tmpl.render(ctx)))
        h = {"Content-type": "application/x-www-form-urlencoded"}
        p = [(k, v) for k, v in json.loads(tmpl.render(ctx)).items()]
        r = requests.post(order.project.pb_url, data =p, headers=h)
