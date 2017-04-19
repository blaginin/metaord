from django.db import models
from django.contrib.auth.models import User
import datetime
import uuid
from webms.models import Webms


class Chief(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bank_account = models.IntegerField()

    def __str__(self):
        return "{0} {1}".format(self.user.first_name, self.user.last_name)



class Project(models.Model):
    name = models.CharField(max_length=512, verbose_name="Название")
    pb_order_create = models.TextField(verbose_name="Тело post-back сообщения при создании заказа в формате JSON", blank=True)
    pb_order_upd_status = models.TextField(verbose_name="Тело post-back сообщения при обновлении статуса заказа в формате JSON", blank=True)
    pb_url = models.URLField(verbose_name="Post-back URL", blank=True)

    author = models.ForeignKey(Chief, null=True) #models.OneToOneField(Chief, default=getdef )
    # contacts = models.CharField(max_length=256, verbose_name="Контакты", default="") # TODO

    @property
    def get_num_orders(self):
        from metaord.models import Order
        return Order.objects.filter(project=self.pk).count()

    @property
    def get_num_confirmed_orders(self):
        from metaord.models import Order, STATUS_CHOICES
        return Order.objects.filter(project=self.pk, status=STATUS_CHOICES[1][0]).count()

    @property
    def get_num_orders_today(self):
        from metaord.models import Order
        return Order.objects.filter(project=self.pk, post_date__gte=datetime.date.today()).count()

    def __str__(self):
        return self.name

WEBMS_INV_STATUS_CHOICES_AND_CLASS = [
    (1,       'Новый',                  'label-primary'),
    (2,       'Принят',                 'label-success'),
    (3,       'Отклонён',               'label-warning'),
]
WEBMS_INV_STATUS_CHOICES = list(map(lambda x: x[0:2], WEBMS_INV_STATUS_CHOICES_AND_CLASS))

class WebmsInvite(models.Model):
    api_token = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    webms = models.ForeignKey(Webms, on_delete=models.CASCADE, verbose_name="Web-мастер")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Проект")
    status = models.IntegerField(choices=WEBMS_INV_STATUS_CHOICES, default=1, verbose_name="Статус приглашения")
    orders_amt = models.IntegerField(default=0, verbose_name="Заказов от приглашения")

    def __str__(self):
        return "Приглашение `{0} {1}` в проект `{2}`".format(self.webms.user.first_name, self.webms.user.last_name, self.project)
