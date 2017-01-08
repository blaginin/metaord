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

    o = Order.objects.create(project=invite.project, status=1, fields=fields_dicts)

    return ApiResponse.success()