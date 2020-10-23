from django.test import TestCase, Client
from .forms import AddProductForm, ReviewForm
from django.shortcuts import reverse


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


# class TestProductViews(TestCase):
#     def test_all_product(self):
#         client = Client()
#         response = client.get('/products/add_product/')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'products/add_product.html')
