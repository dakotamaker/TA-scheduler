from django.test import TestCase
from ..models import Account
from ..domain.CommandHandler import CommandHandler


class LogoutTestCases(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.user = Account.objects.create(act_email='user@email.com', role_id=1, act_password='test')

    def test_logging_in_given_valid_credentials_then_current_user_is_updated(self):
        self.ch.ProcessCommand('login user@email.com test')
        self.assertEqual(self.ch.currentUser, self.user)

    def test_logging_in_given_invalid_password_then_error_occurs(self):
        msg = self.ch.ProcessCommand('login user@email.com wrong_password')
        self.assertEqual(msg, 'Invalid credentials')

    def test_logging_in_given_invalid_username_then_error_occurs(self):
        msg = self.ch.ProcessCommand('login wrong@email.com test')
        self.assertEqual(msg, 'Given email does not belong to an existing user')

    def test_logging_in_given_too_many_parameters_then_error_occurs(self):
        msg = self.ch.ProcessCommand('login wrong@email.com test hello')
        self.assertEqual(msg, 'Invalid number of arguments')

    def test_logging_in_given_too_few_parameters_then_error_occurs(self):
        msg = self.ch.ProcessCommand('login wrong@email.com')
        self.assertEqual(msg, 'Invalid number of arguments')