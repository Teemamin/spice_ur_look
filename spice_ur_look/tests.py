from django.test import TestCase, Client
from products.models import Product
from products.models import Wishlist


class TestHomeView(TestCase):
    def test_all_product(self):
        client = Client()
        response = client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


