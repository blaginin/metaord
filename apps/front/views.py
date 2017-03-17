from django.shortcuts import render, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import redirect
from metaord.utils.auth import Groups
import logging


# logger = logging.getLogger(__name__) # todo

def index(request):
    return render(request, 'front/index.html', {})

def api_doc(request):
	return render(request, 'front/api_doc.html', {})

def msg_logout(request, *args, **kwargs):
    messages.success(request, 'Вы вышли из профиля')
    return auth_views.logout(request, *args, **kwargs)

def home(request, *args, **kwargs):
    assert request.user.is_authenticated()
    url = '/chief' if Groups.is_user_chief(request.user) else '/worker'
    return redirect(url, args, kwargs)
