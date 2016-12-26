from django.test import TestCase
from django.test import Client
from django.db.utils import IntegrityError
from metaord.models import Order, STATUS_CHOICES
from metaord.utils.auth import *
from chief.models import Project

class ProjectIntegrationTestCase(TestCase):
    PROJECTS_PATH = "/chief/projects/"
    PROJECT_PATH = lambda self, pk: "/chief/project/" + str(pk) + "/"

    chief = None
    worker = None
    proj1 = None
    proj2 = None
    c = Client()
    # use random sting to pevent accidental `self.assertContains` match
    p1_name = "p1_y3SWjtuyghjagf212"
    p2_name = "p2_poifj32hgfsdaa2"

    def setUp(self):
        self.chief = User.objects.create_user(username="ch", email="c@h.ru", password="123")
        self.chief.groups.add(Groups.get_or_create_chief())
        self.worker = User.objects.create_user(username="wr", email="w@h.ru", password="123")
        self.worker.groups.add(Groups.get_or_create_worker())

        self.proj1 = Project.objects.create(name=self.p1_name)
        self.proj2 = Project.objects.create(name=self.p2_name)
        Order.objects.create(project=self.proj1, status=2)
        Order.objects.create(project=self.proj2, status=1)

    def test_accesProject_chief(self):
        self.c.login(username="ch", password="123")

        resp1 = self.c.get(self.PROJECT_PATH(self.proj1.pk))
        self.assertEqual(resp1.status_code, 200)
        # print(resp1.content.decode("utf8"))
        self.assertContains(resp1, self.p1_name)
        self.assertNotContains(resp1, self.p2_name)

        resp2 = self.c.get(self.PROJECT_PATH(self.proj2.pk))
        self.assertEqual(resp2.status_code, 200)
        self.assertContains(resp2, self.p2_name)
        self.assertNotContains(resp2, self.p1_name)

    def test_accesProjects_chief(self):
        self.c.login(username="ch", password="123")
        resp = self.c.get(self.PROJECTS_PATH)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.p1_name)
        self.assertContains(resp, self.p2_name)

    def test_notAccesProjects_worker(self):
        self.c.login(username="wr", password="123")
        resp = self.c.get(self.PROJECTS_PATH)
        self.assertEqual(resp.status_code, 302)
