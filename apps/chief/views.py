from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView, TemplateView, UpdateView, CreateView, DeleteView
from django.contrib import auth, messages
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_GET, require_POST
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.utils import timezone
from metaord.views import OrderList, OrderCreate as BaseOrderCreate
from metaord.forms import UserForm, build_order_form_class
from metaord.models import OrderField, Order, STATUS_CHOICES_AND_CLASS
from metaord.utils.view import ExtraContext
from metaord.utils.auth import Groups
from metaord.utils.models import create_default_order_fields
from metaord.utils.decorators import group_required, class_decorator
from chief.models import WebmsInvite, Project, Chief
from chief.forms import ChiefForm
from functools import partial
# todo: mb distribute by files

login_url = reverse_lazy("login")

@group_required("chief", login_url=login_url)
def index(request):
    return render(request, "chief/index.html", {})


@class_decorator(group_required("chief", login_url=login_url))
class ProjectList(ListView):
    model = Project
    template_name = "chief/projects/projects.html"

    def get_queryset(self):
        return super(ProjectList, self).get_queryset().filter(author=Chief.objects.all().get(user=self.request.user))

@class_decorator(group_required("chief", login_url=login_url))
class ProjectDetails(OrderList):
    template_name = "chief/projects/project.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["project"] = Project.objects.get(pk=self.kwargs["pk"])
        ctx["webms_invites"] = WebmsInvite.objects.filter(project=ctx["project"])
        ctx["extra_fields"] = { field.name : str(field.pk) for field in OrderField.objects.filter(project=ctx["project"]) }
        ctx.update()
        return ctx

    def get_queryset(self):
        qset = super().get_queryset()
        return qset.filter(project=self.kwargs["pk"])

@class_decorator(group_required("chief", login_url=login_url))
class ProjectCreate(SuccessMessageMixin, CreateView):
    model = Project
    template_name = "chief/projects/create.html"
    fields = ["name", "pb_order_create", "pb_order_upd_status", "pb_url"]
    success_url = reverse_lazy("chief:projects")
    success_message = "Проект успешно создан"

    def form_valid(self, form):
        proj = form.save()

        proj.author = Chief.objects.all().get(user=self.request.user)
        # print('PA', proj.author)
        proj.save()
        
        create_default_order_fields(proj)
        return HttpResponseRedirect(reverse_lazy("chief:project", kwargs={"pk": proj.pk}))

@class_decorator(group_required("chief", login_url=login_url))
class ProjectUpdate(SuccessMessageMixin, UpdateView):
    model = Project
    template_name = "chief/projects/update.html"
    fields = "__all__"
    success_url = reverse_lazy("chief:projects")
    success_message = "Проект успешно изменён"

@class_decorator(group_required("chief", login_url=login_url))
class ProjectDelete(SuccessMessageMixin, DeleteView):
    model = Project
    template_name = "chief/projects/delete.html"
    fields = "__all__"
    success_url = reverse_lazy("chief:projects")
    success_message = "Проект успешно удалён"


@class_decorator(group_required("chief", login_url=login_url))
class OrderCreate(TemplateView):
    template_name = "chief/orders/create.html"
    success_url = reverse_lazy("chief:projects")
    success_message = "Заказ успешно создан"
    Form = None
    initial = None
    proj_order_fields = []

    def dispatch(self, *args, **kwargs):
        """Construct Form class and set initial if exists"""
        self.proj_order_fields = OrderField.objects.filter(project=self.kwargs["project_pk"])
        self.Form = build_order_form_class(self.proj_order_fields)
        if "order_pk" in self.kwargs:
            order = Order.objects.get(pk=self.kwargs["order_pk"])
            self.initial = {
                "project": order.project.pk,
                "status": order.status,
                "post_date": order.post_date,
            }
            self.initial.update(order.fields)
        return super(OrderCreate, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        form_init = self.initial or {"project": self.kwargs["project_pk"]}
        order_form = self.Form(initial=form_init)
        return render(request, self.template_name, {"form": order_form})

    def post(self, request, *args, **kwargs):
        form = self.Form(request.POST)
        if form.is_valid():
            extra_fields = { str(field.pk) : form.cleaned_data[str(field.pk)] for field in self.proj_order_fields }
            if "order_pk" in self.kwargs:
                o = Order.objects.get(pk=self.kwargs["order_pk"])
                o.project=form.cleaned_data["project"]
                o.status=form.cleaned_data["status"]
                o.fields=extra_fields
                # print('******', o.pk, o.id)
                o.save()
            else:
                # print('(a)')
                o = Order(project=form.cleaned_data["project"], status=form.cleaned_data["status"], fields=extra_fields)
                # print('(b)')
                o.save()
                # print('^^^^ NO',o.pk, o)

            messages.success(request, self.success_message)
            return redirect(reverse_lazy("chief:project", kwargs={"pk": self.kwargs["project_pk"]}), request=request)
        else:
            return render(request, self.template_name, {"form": form})

@class_decorator(group_required("chief", login_url=login_url))
class OrderUpdate(OrderCreate):
    template_name = "chief/orders/update.html"
    success_message = "Заказ успешно обновлён"

@class_decorator(group_required("chief", login_url=login_url))
class OrderDelete(SuccessMessageMixin, DeleteView):
    model = Order
    template_name = "chief/orders/delete.html"
    success_url = reverse_lazy("chief:projects")
    success_message = "Заказ успешно удалён"

    def get_object(self, queryset=None):
        obj = super(OrderDelete, self).get_object(queryset)
        if obj != None:
            self.success_url = reverse_lazy("chief:project", kwargs={"pk": obj.project.pk})
        return obj

@class_decorator(group_required("chief", login_url=login_url))
class OrderFieldList(ListView):
    model = OrderField
    template_name = "chief/orders/fields/list.html"

    def get_context_data(self, **kwargs):
        ctx = super(OrderFieldList, self).get_context_data(**kwargs)
        ctx["project_pk"] = self.kwargs["project_pk"]
        ctx.update()
        return ctx

    def get_queryset(self, **kwargs):
        qset = super(OrderFieldList, self).get_queryset(**kwargs)
        return qset.filter(project=self.kwargs["project_pk"])

@class_decorator(group_required("chief", login_url=login_url))
class OrderFieldCreate(SuccessMessageMixin, CreateView):
    model = OrderField
    fields = "__all__"
    template_name = "chief/orders/fields/create.html"
    success_url = reverse_lazy("chief:projects")
    success_message = "Поле успешно создано"

    def get_initial(self):
        proj = get_object_or_404(Project, pk=self.kwargs["project_pk"])
        return {'project': proj}

    def get_context_data(self, **kwargs):
        ctx = super(OrderFieldCreate, self).get_context_data(**kwargs)
        ctx["project_pk"] = self.kwargs["project_pk"]
        ctx.update()
        return ctx

    def form_valid(self, form):
        self.success_url = reverse_lazy("chief:project", kwargs={"pk": form.instance.project.pk})
        return super(OrderFieldCreate, self).form_valid(form)

@class_decorator(group_required("chief", login_url=login_url))
class OrderFieldUpdate(SuccessMessageMixin, UpdateView):
    model = OrderField
    template_name = "chief/orders/fields/update.html"
    fields = "__all__"
    success_url = reverse_lazy("chief:projects")
    success_message = "Поле успешно изменено"

    def form_valid(self, form):
        self.success_url = reverse_lazy("chief:project", kwargs={"pk": form.instance.project.pk})
        return super(OrderFieldUpdate, self).form_valid(form)

@class_decorator(group_required("chief", login_url=login_url))
class OrderFieldDelete(SuccessMessageMixin, DeleteView):
    model = OrderField
    template_name = "chief/orders/fields/delete.html"
    success_url = reverse_lazy("chief:projects")
    success_message = "Поле успешно удалено"

    def get_object(self, queryset=None):
        obj = super(OrderFieldDelete, self).get_object(queryset)
        if obj != None:
            self.success_url = reverse_lazy("chief:project", kwargs={"pk": obj.project.pk})
        return obj


@class_decorator(group_required("chief", login_url=login_url))
class InviteList(ListView):
    model = WebmsInvite
    template_name = "chief/projects/webms_invites.html"

    def get_queryset(self):
        qset = super().get_queryset()
        return qset.filter(project=self.kwargs["project_pk"])


@class_decorator(group_required("chief", login_url=login_url))
class InviteCreate(SuccessMessageMixin, CreateView):
    model = WebmsInvite
    fields = ["webms", "project"]
    template_name = "chief/webms_invites/create.html"
    success_url = reverse_lazy("chief:projects")
    success_message = "Приглашение успешно создано"

    def form_valid(self, form):
        self.success_url = reverse_lazy("chief:project", kwargs={"pk": form.instance.project.pk})
        return super(InviteCreate, self).form_valid(form)

@class_decorator(group_required("chief", login_url=login_url))
class InviteDelete(SuccessMessageMixin, DeleteView):
    model = WebmsInvite
    template_name = "chief/webms_invites/delete.html"
    success_url = reverse_lazy("chief:projects")
    success_message = "Приглашение успешно удалёно"

    def get_object(self, queryset=None):
        obj = super(InviteDelete, self).get_object(queryset)
        if obj != None:
            self.success_url = reverse_lazy("chief:project", kwargs={"pk": obj.project.pk})
        return obj


class RegistrationView(TemplateView):
    template_name = "chief/register.html"

    def get(self, request, *args, **kwargs):
        super(RegistrationView, self).get(request, args, kwargs)
        user_form = UserForm()
        chief_form = ChiefForm()
        return render(request, self.template_name, {"user_form": user_form, "chief_form": chief_form})

    def post(self, request):
        user_form = UserForm(request.POST)
        chief_form = ChiefForm(request.POST)
        if user_form.is_valid() * chief_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(request.POST.get('password')) # todo: mb cleanded data
            user.save()
            chief = chief_form.save(commit=False)
            chief.user = user
            chief.save()
            user.groups.add(Groups.get_or_create_chief())
            messages.success(request, 'Предпринематель успешно зарегистрирован.')
            return redirect('/chief/', request=request)
        else:
            return render(request, self.template_name, {"user_form": user_form, "chief_form": chief_form})
