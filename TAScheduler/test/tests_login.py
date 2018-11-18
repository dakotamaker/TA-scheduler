from django.test import TestCase
from ..models import Account
from ..domain import CommandHandler

# Create your tests here.
class LoginTestCase(TestCase):
    def setUp(self):
        Account.objects.create(act_email='email@email.com', act_fname='dorris', act_lname='fudge',
                               act_password='password', act_address='123 main st.', act_phone='123-123-1234', role_id=2,
                               act_officehours="11-12", act_officelocation="EMS 123")
        # self.ch = CommandHandler
    #not working
    # def test_login(self):
