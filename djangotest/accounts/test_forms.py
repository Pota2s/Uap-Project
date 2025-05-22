from django.test import TestCase
from .models import CustomUser
from .forms import CustomUserCreationForm

class CustomUserCreationFormTests(TestCase):

    def setUp(self):
        self.form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }

    def test_form_validity(self):
        form = CustomUserCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_user_creation(self):
        form = CustomUserCreationForm(data=self.form_data)
        if form.is_valid():
            user = form.save()
            self.assertIsInstance(user, CustomUser)
            self.assertEqual(user.username, 'testuser')
            self.assertEqual(user.email, 'testuser@example.com')
            self.assertTrue(user.check_password('testpassword'))