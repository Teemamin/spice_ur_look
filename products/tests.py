from django.test import TestCase, Client
from .forms import AddProductForm, ReviewForm
from .models import Product
from django.shortcuts import reverse, get_object_or_404


# Create your tests here.


class TestProductForms(TestCase):
    def test_form_isvalid(self):
        form_data = {
            'name': 'item',
            'gender': "man",
            'description': 'test',
            'price': 22.99,
            'rating': 3,
            'quantity': 1,
        }
        form = AddProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_required_fields(self):
        form_data = {
            'name': 'item',
            'gender': "man",
            'rating': 3,
            'quantity': 1,
        }
        form = AddProductForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestReviewForms(TestCase):
    def test_form_valid(self):
        form_data = {
            'review': 'test fields',
            'rate': 2,
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_rate_required(self):
        form_data = {
            'review': 'test fields',
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestProductViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.products_url = reverse('products')

    def test_all_product(self):
        response = self.client.get(self.products_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_single_product_path(self):
        product = Product.objects.create(
            name='testing edit',
            gender='man',
            description='test desc',
            price=20.2,
            quantity=1
        )
        response = self.client.get(f'/products/{product.id}/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/single_product.html')

    def test_add_product(self):
        form = AddProductForm({
            'name': 'added',
            'gender': 'man',
            'description': 'test desc',
            'price': 20.2,
            'quantity': 1,
            'rating': 3,
        })
        self.client.post('/add_product/')
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
        form.save()
        new_product = get_object_or_404(Product, name='added')
        self.assertTrue(new_product)


