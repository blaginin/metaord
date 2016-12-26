from django.test import TestCase
from django.test import Client
from django.db.utils import IntegrityError
import json
import requests
from api.models import ErrCodes
from metaord.utils.auth import *
from metaord.models import Project, OrderField, Order
from webms.models import Webms
from chief.models import WebmsInvite

class ApiOrdersTestCase(TestCase):
    c = Client()
    webms = None
    proj1 = None
    invite = None
    fields = {}

    def setUp(self):
        r = requests.get("http://elastic-ass.ru/test.php", json={"key": "value"})
        print(r)
        u = User.objects.create_user(username="test_wm", first_name="test_user", email="w@h.ru", password="123")
        u.groups.add(Groups.get_or_create_webms())
        self.webms = Webms.objects.create(user=u)

        self.proj1 = Project.objects.create(name="test_p1")
        self.invite = WebmsInvite.objects.create(project=self.proj1, webms=self.webms)
        self.fields["test_FIO"] = OrderField.objects.create(project=self.proj1, name="test_FIO", vtype=1,
            pattern=r".{3,128}", error_msg="некорректное test_FIO", is_required=True)
        self.fields["test_email"] = OrderField.objects.create(project=self.proj1, name="test_email", vtype=1, pattern=r".{3,128}", error_msg="email incorrect")
        self.fields["phone"] = OrderField.objects.create(project=self.proj1, name="phone", vtype=2, pattern=r"\d+", error_msg="phone incorrect")
        data_json = json.dumps({ "api_token": str(self.invite.api_token),
            "order": { "test_FIO": "Альберт Бикеев", "test_email": "a@b.ru", "phone": 12356, }
        })
        self.c.post("/api/order/create/", data=data_json, content_type="application/json")


    def test_orderCreated(self):
        created_ord = Order.objects.filter(fields__has_key=str(self.fields["test_FIO"].pk)).first()
        self.assertTrue(created_ord is not None)
        self.assertEqual(created_ord.fields[str(self.fields["test_email"].pk)], "a@b.ru")

    def test_createOrder_correct(self):
        data_json = json.dumps({ "api_token": str(self.invite.api_token),
            "order": { "test_FIO": "Альберт 123", "test_email": "a@b.ru", "phone": 12356, }
        })
        resp = self.c.post("/api/order/create/", data=data_json, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.content.decode("utf-8"))
        self.assertEqual(resp_data["is_success"], True)

    def test_createOrder_incorrectOrderFormat(self):
        data_json = json.dumps({ "api_token": str(self.invite.api_token),
            "order": { "test_FIO": "B", "test_email": "a@b.ru", "phone": "abc12356", }
        })
        resp = self.c.post("/api/order/create/", data=data_json, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.content.decode("utf-8"))
        self.assertEqual(resp_data["is_success"], False)
        self.assertTrue(self.fields["test_FIO"].error_msg in resp_data["form_errors"])
        self.assertTrue(self.fields["phone"].error_msg in resp_data["form_errors"])

    def test_createOrder_incorrectReqFormat_incorrectToken(self):
        data_json = json.dumps({ "api_token": "0dc0c8c2-be0a-41a0-9eb1-86879",
            "order": { "test_email": "a@b.ru", "phone": 12356, }
        })
        resp = self.c.post("/api/order/create/", data=data_json, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.content.decode("utf-8"))
        self.assertEqual(resp_data["is_success"], False)
        self.assertEqual(resp_data["error_code"], ErrCodes.token_err)
