from django.test import TestCase, Client
from django.shortcuts import reverse
from products.models import Product

from django.contrib.auth.models import User

# Create your tests here.


class TestBagViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword'
        )
        self.shopping_bag_url = reverse('shopping_bag')

    def test_shopping_bag_view(self):
        response = self.client.get(self.shopping_bag_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopping_bag/shopping_bag.html')

    def test_add_to_shopping_bag(self):
        product = Product.objects.create(
            name='testing edit',
            gender='man',
            description='test desc',
            price=20.2,
            quantity=1
        )
        self.client.post(
            '/shopping_bag/add/', {' product_id': product.id, 'quantity': 1}
        )

    def test_alter_shoping_bag(self):
        product = Product.objects.create(
            name='testing edit',
            gender='man',
            description='test desc',
            price=20.2,
            quantity=1
        )
        self.client.post(
            '/shopping_bag/remove_from_bag/',
            {' product_id': product.id, 'quantity': 1}
        )

    def test_remove_from_bag(self):
        product = Product.objects.create(
            name='testing edit',
            gender='man',
            description='test desc',
            price=20.2,
            quantity=1
        )
        self.client.post(
            '/shopping_bag/alter_shoping_bag/', {' product_id': product.id}
        )

