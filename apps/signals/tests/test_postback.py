import socket
import sys
# from mock import patch
from unittest.mock import MagicMock, patch
from django.db.models.signals import pre_save
from django.test import TestCase
from django.test import Client
from django.db.utils import IntegrityError
import json
from signals.handlers import do_postback
from metaord.utils.auth import *
from metaord.models import Project, OrderField, Order


class ApiOrdersTestCase(TestCase):
    c = Client()
    webms = None
    proj1 = None
    invite = None
    fields = {}

    pb_address = ('localhost', 10000)
    sock = socket.socket()
    recved_data = None
    pb_tosend_msg = """
        {
            "status": {{ order.status }}
        }
    """

    def setUp(self):
        pass

        #self.handler = MagicMock()
        #do_postback.connect(handler, sender='test')


    # todo

    # def test_cache(self):
    #     with patch('signals.handlers.do_postback', autospec=True) as mocked_handler:
    #         pre_save.connect(mocked_handler, sender=None, dispatch_uid='test_cache_mocked_handler')
    #         self.proj1 = Project.objects.create(name="test_pb_p1", pb_order_create=self.pb_tosend_msg, pb_url="localhost:10000")
    #         self.fields["test_FIO"] = OrderField.objects.create(project=self.proj1, name="test_FIO", vtype=1,
    #             pattern=r".{3,128}", error_msg="некорректное test_FIO", is_required=True)
    #         self.fields["test_email"] = OrderField.objects.create(project=self.proj1, name="test_email", vtype=1, pattern=r".{3,128}", error_msg="email incorrect")
    #         self.fields["phone"] = OrderField.objects.create(project=self.proj1, name="phone", vtype=2, pattern=r"\d+", error_msg="phone incorrect")
    #         extra_fields = {}
    #         extra_fields[self.fields["test_FIO"].pk] = "Test Testing"
    #         extra_fields[self.fields["test_email"].pk] = "t@pb.ru"
    #         extra_fields[self.fields["phone"].pk] = "9583425835"
    #         Order.objects.create(project=self.proj1, status=1, fields=extra_fields)
    #     print(mocked_handler)
    #     self.assertEquals(mocked_handler.call_count, 1)

        # self.sock.bind(self.pb_address)
        # self.sock.listen(1)
        # print('waiting for a connection')
        # connection, client_address = self.sock.accept()
        # with connection:
        #     print('connection from', client_address)
        #     self.recved_data = connection.recv(1024)
        #     print('received {!r}'.format(self.recved_data))
        #self.sock.connect(self.host_and_port)
        # self.recved_data = sock.recv()

    #def test_dummy(self):

        # Create handler
        #self.handler.assert_called_once_with(signal=do_postback)

