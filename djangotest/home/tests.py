from django.test import TestCase,Client
from home.models import User,UserTransaction
from datetime import date
from django.http import HttpResponse
# Create your tests here.

class InitializationTestCase(TestCase):
    def setUp(self):
        User.objects.create(user_name="test",user_password="awa",date_of_birth="2005-09-03")

    def test_initial_user_has_zero_balance(self):
        user : User = User.objects.get(user_name="test")
        self.assertEqual(user.user_wallet,0,"User is initialized with non-zero balance")

class AdditionTestCase(TestCase):
    def setUp(self):
        User.objects.create(user_name="test",user_password="awa",date_of_birth=date(2005,9,3))
    
    def test_initial_user_balance_is_added(self):
        user : User = User.objects.get(user_name="test")
        user.wallet = user.wallet + 300.0
        self.assertEqual(user.user_wallet,300.0,"User balance addition sucessful")

class TransactionTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(user_name="test",user_password="awa",date_of_birth=date(2005,9,3))
        otherUser = User.objects.create(user_name="otherTest",user_password="awa",date_of_birth="2005-09-03")
        UserTransaction.objects.create(user=user,transaction_date=date(2025,5,8))
        UserTransaction.objects.create(user=user,transaction_date=date(2025,5,7))
        UserTransaction.objects.create(user=otherUser,transaction_date=date(2025,5,6))

    def test_all_transactions_are_saved(self):
        self.assertLessEqual(len(UserTransaction.objects.all()),3,"Duplicate transactions are detected")
        self.assertGreaterEqual(len(UserTransaction.objects.all()),3,"Not all transactions are saved")

    def test_get_all_transactions_from_user(self):
        user = User.objects.get(user_name="test")
        self.assertEqual(len(UserTransaction.objects.filter(user=user)),2,"Some transactions are misattributed to other users")

class LoginTestCase(TestCase):
    def setUp(self):
        
        User.objects.create(user_name="test",user_password="awa",date_of_birth=date(2005,9,3))
    

    def test_client_get_user_page(self):
        c = Client()
        self.assertContains(response=c.get("/home/users/login/"),text="")

class RegisterTestCase(TestCase):
    def test_user_can_get_to_login(self):
        c = Client()
        response : HttpResponse = c.post("/home/users/register/")
        self.assertContains(response=response,text="")