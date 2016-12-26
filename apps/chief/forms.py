from django.contrib.auth.models import User
from django import forms
from metaord.forms import UserForm
from chief.models import Chief

class ChiefForm(forms.ModelForm):
    class Meta:
        model = Chief
        fields = "__all__" 
        exclude = ['user']
