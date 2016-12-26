from metaord.models import OrderField, MetaordSettings


def create_default_order_fields(proj):
    s = MetaordSettings.objects.create()
    s.id = 1
    s.save()
    # MetaordSettings.objects.create(post_back_url="")
    OrderField.objects.create(project=proj, name="ФИО", vtype=0, error_msg="Ф.И.О. заполнено неверно")
    OrderField.objects.create(project=proj, name="Страна", vtype=0, error_msg="Страна заполнена неверно")
    OrderField.objects.create(project=proj, name="Индекс", vtype=0, pattern=r"\d{5,6}", error_msg="Некорректный индекс, должен состоять из 5 или 6 цифр.")
    OrderField.objects.create(project=proj, name="Регион", vtype=0, error_msg="Регион заполнен неверно")
    OrderField.objects.create(project=proj, name="Город", vtype=0, error_msg="Город заполнен неверно")
    OrderField.objects.create(project=proj, name="Адрес", vtype=0, error_msg="Адрес заполнен неверно")
    OrderField.objects.create(project=proj, name="Телефон", vtype=0, error_msg="Телефон заполнен неверно", is_required=True)
    OrderField.objects.create(project=proj, name="Email", vtype=5, error_msg="Email заполнен неверно")
    OrderField.objects.create(project=proj, name="Количество", vtype=1, error_msg="Количество заполнено неверно")
    OrderField.objects.create(project=proj, name="Комментарий", vtype=2, error_msg="Комментарий заполнено неверно")
    OrderField.objects.create(project=proj, name="Согласен на обработку персональных данных", is_required=True,
        vtype=3, error_msg="Для оформления заказа необходимо согласие на обработку персональных данных")
    OrderField.objects.create(project=proj, name="С условиями покупки ознакомлен", is_required=True,
        vtype=3, error_msg="Вы должны ознакомиться с условиями покупки")

