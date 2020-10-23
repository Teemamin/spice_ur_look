from django.test import TestCase
from .forms import UserProfileForm


# Create your tests here.


class TestProfileForms(TestCase):
    def test_ProfileForm_valid(self):
        form_data = {
            'phone_number': '12345678',
            'city': 'LA',
            'state': 'Cal',
            'postcode': '23453',
        }
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_valid())
