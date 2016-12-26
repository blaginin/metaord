from django.urls import reverse_lazy
from django.contrib import auth, messages
from django.views.generic import TemplateView, ListView, FormView
from django.shortcuts import redirect, reverse, render, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from metaord.utils.decorators import group_required, class_decorator
from metaord.utils.auth import Groups
from metaord.forms import UserForm
from chief.models import WebmsInvite
from chief.models import WEBMS_INV_STATUS_CHOICES_AND_CLASS
from webms.forms import WebmsForm, InviteStatusForm


login_url = reverse_lazy("login")

@group_required("webms", login_url=login_url)
def index(request):
    return render(request, "webms/index.html", {})


@class_decorator(group_required("webms", login_url=login_url))
class InviteList(ListView):
    model = WebmsInvite
    template_name = "webms/invites/invites.html"

    def get_context_data(self, **kwargs):
        context = super(InviteList, self).get_context_data(**kwargs)
        context["webms_invite_statuses"] = WEBMS_INV_STATUS_CHOICES_AND_CLASS
        context["webms_invite_status"] = self.request.GET.get("webms_invite_status")
        return context

    def get_queryset(self):
        status = self.request.GET.get("webms_invite_status")
        if status is None:
            return WebmsInvite.objects.all()
        else:
            return WebmsInvite.objects.filter(status=status)

@class_decorator(group_required('webms', 'chief', login_url=login_url))
class InviteUpdateStatus(SuccessMessageMixin, FormView):
    form_class = InviteStatusForm
    template_name = "webms/invites/upd_status.html"
    success_url = reverse_lazy("webms:invites")
    success_message = "Статус успешно обновлён"

    def form_valid(self, form):
        invite = WebmsInvite.objects.filter(pk=self.kwargs["pk"])
        assert invite is not None
        invite.update(status=form.cleaned_data['new_status'])
        super(InviteUpdateStatus, self).form_valid(form)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(InviteUpdateStatus, self).get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        return context


class RegistrationView(TemplateView):
    template_name = "webms/register.html"

    def get(self, request, *args, **kwargs):
        super(RegistrationView, self).get(request, args, kwargs)
        user_form = UserForm()
        webms_form = WebmsForm()
        return render(request, self.template_name, {"user_form": user_form, "webms_form": webms_form})

    def post(self, request):
        user_form = UserForm(request.POST)
        webms_form = WebmsForm(request.POST)
        if user_form.is_valid() * webms_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(request.POST.get("password"))
            user.save()
            webms = webms_form.save(commit=False)
            webms.user = user
            webms.save()
            user.groups.add(Groups.get_or_create_webms())
            messages.success(request, "Web-мастер успешно зарегистрирован.")
            return redirect(reverse("webms:index"), request=request)
        else:
            return render(request, self.template_name, {"user_form": user_form, "webms_form": webms_form})
