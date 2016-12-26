from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Order
from worker.models import Operator
from chief.models import Chief
from webms.models import Webms


# Define an inline admin descriptor for sub-user models
# which acts a bit like a singleton
class OperatorInline(admin.StackedInline):
    model = Operator
    can_delete = False
    verbose_name_plural = "operator" # todo: rename to worker

class ChiefInline(admin.StackedInline):
    model = Chief
    can_delete = False # todo: what is it
    verbose_name_plural = "chief"

class WebmsInline(admin.StackedInline):
    model = Webms
    can_delete = False
    verbose_name_plural = "webms"

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (OperatorInline, ChiefInline, WebmsInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Order)
