from django.test import TestCase
from ..models import Account
from ..domain.CommandHandler import CommandHandler


class LogoutTestCases(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.user = Account.objects.create(act_email='user@email.com', role_id=1)
        self.ch.currentUser = self.user

    def test_logging_out_when_current_user_is_valid_then_user_is_logged_out(self):
        self.ch.ProcessCommand('logout')
        self.assertEqual(self.ch.currentUser, None)

    def test_logging_out_when_no_user_is_logged_in_then_error_occurs(self):
        self.ch.ProcessCommand('logout')
        msg = self.ch.ProcessCommand('logout')
        self.assertEqual(msg, 'No user is logged in')

    def test_logging_out_with_too_many_arguments_then_error_occurs(self):
        msg = self.ch.ProcessCommand('logout test')
        self.assertEqual(msg, 'Invalid number of arguments')