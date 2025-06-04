from django.test import TestCase
from django.urls import reverse
from .forms import ProductForm,StoreForm
from .models  import Store
from accounts.models import CustomUser

# Create your tests here.
class FormTest(TestCase):
    def setUp(self):
        self.user : CustomUser = CustomUser.objects.create(
            username = 'testuser',
            email= 'testuser@example.com',
            password = 'testpassword'
        )
    
    def test_store_setup(self):
        user = self.user

        form_data : dict = {
            'name' : 'Store_name',
            'description' : 'Store_desc',
        }

        form = StoreForm(data=form_data)
        

        self.assertTrue(form.is_valid())

        store = form.save(commit= False)
        store.owner = user
        store.save()

        if (form.is_valid()):
            self.assertTrue(Store.objects.get(owner = user))
            store : Store = Store.objects.get(owner = user)

            self.assertEqual(store.owner, user)

class ViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.store = Store.objects.create(
            name='Original Store',
            description='Original description',
            owner=self.user
        )
        
    def test_store_create_view(self):
        self.client.login(username = 'testuser',password = 'testpassword') 
        url = reverse('store_create')
        data = {
            'name': 'Test Store',
            'description': 'A test store',
        }
        response = self.client.post(url, data)
        # Check redirect or success
        self.assertEqual(response.status_code, 302)  # or 200 if you render the page again

        # Check the store was created
        store = Store.objects.get(name='Test Store')
        self.assertEqual(store.owner, self.user)
        self.assertEqual(store.description, 'A test store')
    
    def test_store_edit_view(self):
        self.client.login(username = 'testuser',password = 'testpassword') 
        url = reverse('store_edit',args=[self.store.id])
        data = {
            'name': 'Updated Store',
            'description': 'Updated desc',
        }
        response = self.client.post(url, data)
        # Check redirect or success
        self.assertEqual(response.status_code, 302)  # or 200 if you render the page again

        # Check the store was edited
        self.store.refresh_from_db()
        self.assertEqual(self.store.owner, self.user)
        self.assertEqual(self.store.description, 'Updated desc')

    