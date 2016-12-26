from django.contrib.auth.models import User
from django import forms
from .models import Operator
from metaord.models import Order, STATUS_CHOICES


class OperatorForm(forms.ModelForm):
    class Meta:
        model = Operator
        fields = "__all__" 
        exclude = ['user']

class OrderStatusForm(forms.Form):
    new_status = forms.ChoiceField(choices=STATUS_CHOICES)
