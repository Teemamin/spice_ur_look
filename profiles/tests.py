from django.test import TestCase, Client
from .forms import UserProfileForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import reverse

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



# class TestProfileModels(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             'john', 'lennon@thebeatles.com', 'johnpassword',
#             superuser_status=True
#         )

#     def test_userprofile_model_return_name(self):
#         """Test that model returns name"""
#         userprofile = UserProfile.objects.create(
#             user=self.user,
#             phone_number='12345678',
#             city='LA',
#             state='Cal',
#             postcode='23453',
#         )
#         self.assertEqual(userprofile.user.username, 'john')
