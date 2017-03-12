import json
from django.contrib import auth, messages
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from api.models import ApiResponse, ErrCodes, ApiOrder
from chief.models import WebmsInvite, Project
from metaord.models import Order, OrderField, STATUS_CHOICES
from metaord.utils.auth import is_valid_uuid
from django.views.decorators.csrf import csrf_exempt


class Scm():
    """ Order request schema """
    api_token = "api_token"
    order = "order"
    order_id = 'order_id'


@csrf_exempt
def create_order(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except ValueError as err:
        return ApiResponse.failure("Value error: `{0}`.".format(err), ErrCodes.format_err)

    if Scm.api_token not in data:
        return ApiResponse.failure("API token not povided.", ErrCodes.arg_err)

    if Scm.order not in data:
        return ApiResponse.failure("Order not povided.", ErrCodes.arg_err)

    tok = data[Scm.api_token]
    if not is_valid_uuid(tok):
        return ApiResponse.failure("API token is incorrect.", ErrCodes.token_err)

    invite = WebmsInvite.objects.filter(api_token=tok).first()
    if not invite:
        return ApiResponse.failure("No invite matching to API token.", ErrCodes.invite_err)

    fields = OrderField.objects.filter(project=invite.project)
    if not fields:
        return ApiResponse.failure("No fields matching to API token.", ErrCodes.fields_not_created_err)

    fields_dicts, form_errors = ApiOrder.validate_order(data[Scm.order], fields)
    if form_errors:
        return ApiResponse.failure_form_not_valid(form_errors)

    o = Order(project=invite.project, status=0, fields=fields_dicts)
    o.save()
    # print('OOOO&&&&&&&', o.id, o.pk)

    return ApiResponse.success_result({'order_id':o.id})

@csrf_exempt
def change_order_status(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except ValueError as err:
        return ApiResponse.failure("Value error: `{0}`.".format(err), ErrCodes.format_err)

    if Scm.api_token not in data:
        return ApiResponse.failure("API token not povided.", ErrCodes.arg_err)

    if Scm.order_id not in data:
        return ApiResponse.failure("order_id not povided.", ErrCodes.arg_err)

    tok = data[Scm.api_token]
    if not is_valid_uuid(tok):
        return ApiResponse.failure("API token is incorrect.", ErrCodes.token_err)

    invite = WebmsInvite.objects.filter(api_token=tok).first()
    if not invite:
        return ApiResponse.failure("No invite matching to API token.", ErrCodes.invite_err)

    try:
        m_order = Order.objects.filter(project=invite.project, pk=int(data['order_id'])).first()
    except BaseException as e:
        return ApiResponse.failure("Cant find order ({0})".format(e), ErrCodes.fields_not_created_err)

    try:
        m_order.status = int(data['status'])
        m_order.save()
    except BaseException as e:
        return ApiResponse.failure("Cant process changes ({0}).".format(e), ErrCodes.fields_not_created_err)


    return ApiResponse.success_result({'order_id':m_order.id})


@csrf_exempt
def view_order(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except ValueError as err:
        return ApiResponse.failure("Value error: `{0}`.".format(err), ErrCodes.format_err)

    if Scm.api_token not in data:
        return ApiResponse.failure("API token not povided.", ErrCodes.arg_err)


    if 'order_id' not in data.keys():
        return ApiResponse.failure("order_id not povided.", ErrCodes.arg_err)

    tok = data[Scm.api_token]
    if not is_valid_uuid(tok):
        return ApiResponse.failure("API token is incorrect.", ErrCodes.token_err)

    try:
        response = Order.objects.all().get(pk=int(data['order_id'])).fields
    except BaseException as e:
        return ApiResponse.failure("Cant get order from DB", ErrCodes.token_err)

    return ApiResponse.success_result(result=response)



@csrf_exempt
def filter_order(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except ValueError as err:
        return ApiResponse.failure("Value error: `{0}`.".format(err), ErrCodes.format_err)

    if Scm.api_token not in data:
        return ApiResponse.failure("API token not povided.", ErrCodes.arg_err)


    if 'status' not in data.keys():
        return ApiResponse.failure("status not povided.", ErrCodes.arg_err)

    

    tok = data[Scm.api_token]
    if not is_valid_uuid(tok):
        return ApiResponse.failure("API token is incorrect.", ErrCodes.token_err)


    invite = WebmsInvite.objects.filter(api_token=tok).first()
    if not invite:
        return ApiResponse.failure("No invite matching to API token.", ErrCodes.invite_err)


    ans = []

    # try:
    response = Order.objects.all().filter(project=invite.project, status=int(data['status']))
    for i in response: ans.append(i.pk)
    # except BaseException as e:
    #     return ApiResponse.failure("Cant get order from DB", ErrCodes.token_err)

    return ApiResponse.success_result(result=ans)

