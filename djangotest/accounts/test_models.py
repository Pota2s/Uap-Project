from django.test import TestCase
from .models import CustomUser

class CustomUserTests(TestCase):
    def setup(self):
        # Create a new CustomUser instance
        user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        return user

    def test_user_creation(self):
        user = self.setup()
        self.assertIsInstance(user, CustomUser)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('testpassword'))