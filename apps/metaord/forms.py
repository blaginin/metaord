from django.contrib.auth.models import User
from django import forms
from chief.models import Project
from metaord.models import Order, STATUS_CHOICES


class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Подтверждение пароля")
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }

def build_order_form_class(project_order_fields):
    form_fields = {}
    form_fields["project"] = forms.ModelChoiceField(queryset=Project.objects.all(), widget=forms.HiddenInput())
    form_fields["status"] = forms.ChoiceField(choices=STATUS_CHOICES, label="Статус")
    for field in project_order_fields:
        form_fields[str(field.pk)] = field.get_form_field()
    return type('DynamicOrderForm', (forms.Form,), form_fields)
