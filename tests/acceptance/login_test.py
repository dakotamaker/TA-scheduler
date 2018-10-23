import unittest
import json
import os
from src.project import Project

# Current user available:
cwd = os.getcwd()
user_data = cwd + '/tests/resources/mock_users_data.json'
with open(user_data, 'r') as u_data:
    users = json.load(u_data)

INVALID_LOGIN_MESSAGE = 'Sorry, your email or password is incorrect'


class LoginTest(unittest.TestCase):
    def test_given_valid_login__then_user_is_logged_in(self):
        msg = Project.command('login ta@one.com test')
        self.assertEqual(msg, 'Welcome ta one')

    def test_given_valid_email_and_invalid_password__then_user_is_not_logged_in(self):
        msg = Project.command('login ta@one.com hello')
        self.assertEqual(msg, INVALID_LOGIN_MESSAGE)

    def test_given_invalid_email__then_user_is_not_logged_in(self):
        msg = Project.command('login invalid@user.com test')
        self.assertEqual(msg, INVALID_LOGIN_MESSAGE)

    def test_given_valid_login_and_then_another_login_attempt__then_user_notified_there_is_already_someone_logged_in(self):
        Project.command('login ta@one.com test')
        msg = Project.command('login ta@two.com test')
        self.assertEqual(msg, 'Sorry, there is already someone logged in.')

    def test_given_a_new_user_logging_in_for_the_first_time__then_the_user_is_greeted_and_told_to_enter_new_password(self):
        msg = Project.command('login new@user.com')
        self.assertEqual(msg, 'Welcome new user. Please enter your new password:')

    def test_given_too_few_arguments_with_an_old_user__then_user_is_not_logged_in(self):
        msg = Project.command('login ta@one.com')
        self.assertEqual(msg, INVALID_LOGIN_MESSAGE)
    
    def test_given_too_many_arguments__then_user_is_not_logged_in(self):
        msg = Project.command('login ta@one.com tests hello')
        self.assertEqual(msg, 'Sorry, but that is too much information for one user')
