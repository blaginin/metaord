from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Operator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    work_time = models.DurationField(verbose_name="Время работы") # care: hardcoded in migrations

    def __str__(self):
        return "{0} {1}".format(self.user.first_name, self.user.last_name)
