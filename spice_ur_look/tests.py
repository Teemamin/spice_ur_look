from django.test import TestCase, Client
from products.models import Product
from products.models import Wishlist


class TestHomeView(TestCase):
    def test_home_view(self):
        client = Client()
        response = client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_home_path(self):
        client = Client()
        response = client.get('/')
        response.context['products']
        response.context['current_user_prdct_id']

