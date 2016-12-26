from django.test import TestCase
from django.db.utils import IntegrityError
from metaord.models import Order
from chief.models import Project

class OrderTestCase(TestCase):
    author1 = 'lion'
    email1 = 'lion@qwevhj.ru'
    status = 1
    proj = None

    def setUp(self):
        self.proj = Project.objects.create(name='test proj')
        Order.objects.create(project=self.proj, status=self.status)

    def test_canCreateOrder(self):
        has_order = Order.objects.filter(status=self.status).exists()
        self.assertEqual(has_order, True)

    def test_canFetchOrder(self):
        order = Order.objects.get(project=self.proj)
        same_order = Order.objects.get(status=self.status)
        self.assertEqual(self.proj, order.project)
        self.assertEqual(self.status, same_order.status)

    def test_cannotCreateWithoutRequired_project(self):
        self.assertRaises(Project.DoesNotExist, Order.objects.create, project=None)

    def test_cannotCreateWithoutRequired_status(self):
        self.assertRaises(IntegrityError, Order.objects.create, project=self.proj, status=None)
