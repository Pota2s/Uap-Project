from django.test import TestCase
from .models import CustomUser
from .forms import CustomUserCreationForm
from store.models import *
from django.urls import reverse

class CustomUserTests(TestCase):
    def setUp(self):
        # Create a new CustomUser instance
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

        self.form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }

        self.edit_data = {
            'username' : 'testuser_changed',
            'email': 'testuser@example.com'
        }

    def test_user_creation(self):
        user = self.user
        self.assertIsInstance(user, CustomUser)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('testpassword'))


    def test_form_validity(self):
        form = CustomUserCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_user_creation_via_form(self):
        form = CustomUserCreationForm(data=self.form_data)
        if form.is_valid():
            user = form.save()
            self.assertIsInstance(user, CustomUser)
            self.assertEqual(user.username, 'testuser')
            self.assertEqual(user.email, 'testuser@example.com')
            self.assertTrue(user.check_password('testpassword'))

    def test_user_edit_via_form(self):
        form = CustomUserCreationForm(data=self.edit_data)
        if form.is_valid():
            user = form.save()
            self.assertEqual(user.username, 'testuser_changed')
            self.assertEqual(user.email, 'testuser@example.com')

    def test_user_creation_via_site(self):
        self.client.logout()
        url = reverse('signup')

        response = self.client.post(url,self.form_data)

        self.assertEqual(response.status_code,200)
        self.assertTrue(self.client.login(username='testuser',password='testpassword'))
        
        

class StoreAndProductTests(TestCase):
    def setup(self) -> tuple[Store,Product]:
        user = CustomUser.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        store = Store.objects.create(
            owner = user,
            description = "Store_desc",
            name = "Store_name"
        )
        product = Product.objects.create(
            name='Product_name',
            store=store,
            description='Product_desc'
        )

        self.store = store
        self.product = product
        return (store,product)

    def test_store_creation(self):
        data : tuple[Store,Product] = self.setup()
        self.assertEqual(data[0].name,"Store_name")
        self.assertEqual(data[0].description,"Store_desc") 
    
    def test_product_creation(self):
        data : tuple[Store,Product] = self.setup()
        self.assertEqual(data[1].name,"Product_name")
        self.assertEqual(data[1].description,"Product_desc") 

    def test_product_ownership(self):
        data : tuple[Store,Product] = self.setup()
        self.assertEqual(data[0],data[1].store)
