from django.contrib.auth.models import User
from django import forms
from metaord.forms import UserForm
from webms.models import Webms
from chief.models import WEBMS_INV_STATUS_CHOICES

class WebmsForm(forms.ModelForm):
    class Meta:
        model = Webms
        fields = "__all__"
        exclude = ['user']

class InviteStatusForm(forms.Form):
    new_status = forms.ChoiceField(choices=WEBMS_INV_STATUS_CHOICES)

