import unittest
import json
import os
from src.project import Project

# Current user available:
cwd = os.getcwd()
user_data = cwd + '/tests/resources/mock_users_data.json'
with open(user_data, 'r') as u_data:
    users = json.load(u_data)


# All are related to PBI number 25
class LogoutTest(unittest.TestCase):
    def test_given_user_is_already_logged_in__then_user_is_logged_out(self):
        Project.command('login ta@one.com test')
        msg = Project.command('logout')
        self.assertEqual(msg, 'Goodbye, ta one')
    
    def test_given_user_is_not_logged_in__then_error_message_is_displayed(self):
        msg = Project.command('logout')
        self.assertEqual(msg, 'There are no users to sign out')
