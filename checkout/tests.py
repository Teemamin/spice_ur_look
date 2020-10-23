from django.test import TestCase
from .forms import CheckoutOrderForm


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
