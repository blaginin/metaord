from django.db import models
from django.contrib.auth.models import User


class Webms(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_available = models.BooleanField(verbose_name="Готов к работе", default=True)

    def __str__(self):
        return "{0} {1}".format(self.user.first_name, self.user.last_name)