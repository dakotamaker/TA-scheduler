import unittest
from tests.resources.TestDataAccess import TestDataAccess
from src.Account import Account
from src.CommandHandler import CommandHandler


# All are related to PBI number 25
class LogoutTest(unittest.TestCase):
    def setUp(self):
        self.db = TestDataAccess()
        Account.LoadEntity(self.db)
        self.ch = CommandHandler(self.db)

    def test_given_user_is_already_logged_in__then_user_is_logged_out(self):
        self.ch.ProcessCommand('login dfudge@school.edu dfudge12')
        msg = self.ch.ProcessCommand('logout')
        self.assertEqual(msg, 'Logged out')
    
    def test_given_user_is_not_logged_in__then_error_message_is_displayed(self):
        msg = self.ch.ProcessCommand('logout')
        self.assertEqual(msg, 'No user is logged in')
