from django.contrib import auth, messages
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from api.models import ApiResponse
import json


# todo: somekind of auth for security (mb OAuth)
def index(request):
    return ApiResponse.success()
