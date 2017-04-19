from django.contrib.postgres.fields import JSONField
from django.db import models
from django import forms
from django.utils import timezone
from django.core.validators import RegexValidator
from worker.models import Operator
from chief.models import Project


class MetaordSettings(models.Model):
    post_back_url = models.CharField(max_length=1024, default="")


# todo: inside of model
# Do not change order of items.
STATUS_CHOICES_AND_CLASS = [
    (0,       'Новый',            'label-default'),
    (1,       'Принят',           'label-primary'),
    (2,       'Отменён',          'label-warning'),
    (3,       'Отправлен',        'label-primary'),
    (4,       'Ждёт оплаты',      'label-info'),
    (5,       'Оплачен',          'label-success'),
    (6,       'Перевод',          'label-success'),
    (7,       'Возврат',          'label-danger'),
    (8,       'Дубликат',         'label-default'),
    (9,       'Ошибка',           'label-warning'),
]

STATUS_CHOICES = list(map(lambda x: x[0:2], STATUS_CHOICES_AND_CLASS))

class Order(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    post_date = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(choices=STATUS_CHOICES)
    fields = JSONField(blank=True, null=True) # TODO: try rm
    is_new = models.BooleanField(default=True)
    def __str__(self):
        return 'Order #{0} from project `{1}`. Fields:{2}'.format(self.pk, self.project, self.fields)

    class Meta:
        ordering = ['-post_date']


FIELD_TYPES_FORMFIELD = [
    (0,         "Строка",       lambda *args, **kwargs: forms.CharField(max_length=256, *args, **kwargs)),
    (1,         "Число",        lambda *args, **kwargs: forms.IntegerField(*args, **kwargs)),
    (2,         "Текст",        lambda *args, **kwargs: forms.CharField(widget=forms.Textarea, *args, **kwargs)),
    (3,         "Флажок",       lambda *args, **kwargs: forms.BooleanField(*args, **kwargs)),
    (4,         "Время",        lambda *args, **kwargs: forms.TimeField(*args, **kwargs)),
    (5,         "Email",        lambda *args, **kwargs: forms.EmailField(*args, **kwargs)),
    (6,         "Телефон",      lambda *args, **kwargs: forms.CharField(validators=[
        RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Некорректный телефон")], *args, **kwargs)),
]

FIELD_TYPES = list(map(lambda x: x[0:2], FIELD_TYPES_FORMFIELD))

class OrderField(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_on = models.BooleanField(verbose_name="Включено", default=True)
    # is_display_on_table = models.BooleanField(verbose_name="Отображать на странице заказов", default=True)
    name = models.CharField(max_length=256, verbose_name="Имя")
    vtype = models.IntegerField(choices=FIELD_TYPES, verbose_name="Тип")
    is_required = models.BooleanField(verbose_name="Обязательное", default=False)
    pattern = models.CharField(max_length=256, verbose_name="Шаблон", default=".+")
    error_msg = models.CharField(max_length=256, verbose_name="Сообщение об ошибке", default="Одно из полей заполненно неправильно.")
    can_worker_edit = models.BooleanField(verbose_name="Оператор может редактировать", default=True)
    can_webms_view = models.BooleanField(verbose_name="Web-мастер может просматривать", default=True)

    def get_form_field(self):
        fld = FIELD_TYPES_FORMFIELD[self.vtype][2](required=self.is_required, label=self.name)
        fld.validators.append(
            RegexValidator(
                regex=self.pattern,
                message=self.error_msg,
                code='field_{0}_is_invalid'.format(self.name)
            ),
        )
        return fld

    class Meta:
        unique_together = ('project', 'name',)

    def __str__(self):
        return self.name
