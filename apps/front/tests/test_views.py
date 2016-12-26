from django.contrib.auth.models import User, Group, Permission
from django.test import Client
from django.test import TestCase
from metaord.utils.auth import Groups


class ViewsTestCase(TestCase):
    c = None
    worker = None
    chief = None
    is_worker_login = False
    is_chief_login = False

    def setUp(self):
        self.c = Client()

        self.worker = User.objects.create_user(username='wr', password='test')
        self.worker.groups.add(Groups.get_or_create_worker())
        self.is_worker_login = self.c.login(username=self.worker.username, password='test')

        self.chief = User.objects.create_user(username='ch', password='test')
        self.chief.groups.add(Groups.get_or_create_chief())
        self.is_chief_login = self.c.login(username=self.chief.username, password='test')

    def test_indexContent(self):
        response = self.c.get('/')
        self.assertEqual(200, response.status_code)

    def test_login_success(self):
        self.assertTrue(self.is_worker_login)
        self.assertTrue(self.is_chief_login)

    def test_accessWorkerSide(self):
        resp = self.c.get('/worker', follow=True)
        self.assertEqual(200, resp.status_code)

    def test_accessChiefSide(self):
        resp = self.c.get('/chief', follow=True)
        self.assertEqual(200, resp.status_code)
