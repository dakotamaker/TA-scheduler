from django.test import TestCase
from ..models import Account
from ..views import index
from ..domain.ErrorMessages import ErrorMessages
# Create your tests here.
class LoginTestCase(TestCase):
    def setUp(self):
        Account.objects.create(act_email='email@email.com', act_fname='dorris', act_lname='fudge',
                               act_password='password', act_address='123 main st.', act_phone='123-123-1234', role_id=2,
                               act_officehours="11-12", act_officelocation="EMS 123")
        Account.objects.create(act_email='new@user.com', act_fname='test', act_lname='test',
                               act_password='', act_address='123 main st.', act_phone='123-123-1234', role_id=2,
                               act_officehours="11-12", act_officelocation="EMS 123")

    def test_given_valid_login__then_user_is_logged_in(self):
        msg = index('login email@email.com password').return_str
        self.assertEqual(msg, 'Logged in as email@email.com')

    def test_given_valid_email_and_invalid_password__then_user_is_not_logged_in(self):
        msg = index('login email@email.com invalid').return_str
        self.assertEqual(msg, 'Invalid credentials')

    def test_given_invalid_email__then_user_is_not_logged_in(self):
        msg = index('login invalid@user.com test').return_str
        self.assertEqual(msg, 'Given email does not belong to an existing user')

    def test_given_a_new_user_logging_in_for_the_first_time__then_the_user_is_greeted_and_their_password_is_saved(self):
        msg = index('login new@user.com test').return_str
        self.assertEqual(msg, 'Logged in as new@user.com, your new password has been saved')

    def test_given_too_few_arguments_with_an_old_user__then_user_is_not_logged_in(self):
        msg = index('login test@test.com').return_str
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)

    def test_given_too_many_arguments__then_user_is_not_logged_in(self):
        msg = index('login test@test.com hello world').return_str
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
