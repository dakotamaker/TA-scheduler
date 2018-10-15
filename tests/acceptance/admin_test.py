import unittest
from src.project import Project

# Current user available:
user = [{'firstName': 'foo', 'lastName': 'bar', 'email': 'foo@bar.com', 'password': 'tests', 'currentUser': 'true'}]


class AdminTest(unittest.TestCase):
    def test_given_user_is_already_logged_in__then_user_is_logged_out(self):
        Project.command('login foo@bar.com tests')
        msg = Project.command('logout')
        self.assertEqual(msg, 'Goodbye, foo bar')
    
    def test_given_user_is_not_logged_in__then_error_message_is_displayed(self):
        msg = Project.command('logout')
        self.assertEqual(msg, 'There are no users to sign out')