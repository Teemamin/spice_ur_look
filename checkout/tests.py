from django.test import TestCase, Client
from django.shortcuts import reverse
from .forms import CheckoutOrderForm
from django.contrib.auth.models import User
from shopping_bag.models import Bag
from.models import Order


# Create your tests here.


class TestCheckoutOrderForms(TestCase):
    def test_full_name_is_required(self):
        form = CheckoutOrderForm({'full_name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors.keys())
        self.assertEqual(
            form.errors['full_name'][0], 'This field is required.'
        )

    def test_email_is_required(self):
        form = CheckoutOrderForm({'email': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())
        self.assertEqual(form.errors['email'][0], 'This field is required.')

    def test_fields_explicit_in_form_metaclass(self):
        form = CheckoutOrderForm()
        self.assertEqual(form.Meta.fields, (
            'full_name', 'email', 'phone_number',
            'address_1', 'address_2',
            'city', 'state', 'postcode', 'country', ))

    def test_address_1_is_required(self):
        form = CheckoutOrderForm({'address_1': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('address_1', form.errors.keys())
        self.assertEqual(
            form.errors['address_1'][0], 'This field is required.'
        )

    def test_country_is_required(self):
        form = CheckoutOrderForm({'country': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('country', form.errors.keys())
        self.assertEqual(
            form.errors['country'][0], 'This field is required.'
        )

    def test_CheckoutOrderForm_valid(self):
        form_data = {
            'full_name': 'susu',
            'email': "user@mp.com",
            'phone_number': '12345678',
            'address_1': 'test address',
            'address_2': "fkgns",
            'city': 'LA',
            'state': 'Cal',
            'postcode': '23453',
            'country': 'US',
        }
        form = CheckoutOrderForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestCheckoutViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword'
        )
        self.checkout_url = reverse('checkout')

    def test_checkout_view(self):
        response = self.client.get(self.checkout_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopping_bag/shopping_bag.html')

    def test_checkout_success(self):
        response = self.client.get('checkout/success/',  follow=True)
        self.assertTemplateNotUsed(response, 'checkout/success.html')

class TestCheckoutOrderModels(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword'
        )

    def test_order_model(self):
        bag = Bag.objects.create(
            user=self.user,
            subtotal=2.44,
            total=22.3
        )
        order = Order.objects.create(
            full_name='susu',
            email="user@mp.com",
            bag=bag,
            phone_number='12345678',
            address_1='test address',
            address_2="fkgns",
            city='LA',
            state='Cal',
            postcode='23453',
            country='US',
        )
        order.save()
        self.assertEqual(order.order_number, order.order_number)
