from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import *
import json


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')

    def test_home_GET(self):

        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'accounts/templates/accounts/dashboard.html')
