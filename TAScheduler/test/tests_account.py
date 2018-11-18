from django.test import TestCase
from ..models import Account


# Create your tests here.
class AccountTestCase(TestCase):
    def setUp(self):
        Account.objects.create(act_email='email@email.com', act_fname='dorris', act_lname='fudge',
                               act_password='password', act_address='123 main st.', act_phone='123-123-1234', role_id=2,
                               act_officehours="11-12", act_officelocation="EMS 123")

    def test_account(self):
        a = Account.objects.get(act_email="email@email.com")
        self.assertEqual(a.act_fname, 'dorris')