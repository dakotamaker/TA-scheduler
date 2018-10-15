import unittest
from src.project import Project

# Current user available:
user = [
    {'firstName': 'foo', 'lastName': 'bar', 'email': 'foo@bar.com', 'password': 'tests', 'currentUser': False},
    {'firstName': 'tests', 'lastName': 'tests', 'email': 'tests@tests.com', 'password': 'tests', 'currentUser': False},
    {'firstName': 'hello', 'lastName': 'world', 'email': 'hello@world.com', 'password': '', 'currentUser': False}
]

INVALID_LOGIN_MESSAGE = 'Sorry, your email or password is incorrect'


# All are related to PBI number 25
class LoginTest(unittest.TestCase):
    def test_given_valid_login__then_user_is_logged_in(self):
        msg = Project.command('login foo@bar.com tests')
        self.assertEqual(msg, 'Welcome foo bar')

    def test_given_valid_email_and_invalid_password__then_user_is_not_logged_in(self):
        msg = Project.command('login foo@bar.com hello')
        self.assertEqual(msg, INVALID_LOGIN_MESSAGE)

    def test_given_invalid_email__then_user_is_not_logged_in(self):
        msg = Project.command('login bar@foo.com tests')
        self.assertEqual(msg, INVALID_LOGIN_MESSAGE)

    def test_given_valid_login_and_then_another_login_attempt__then_user_notified_there_is_already_someone_logged_in(self):
        Project.command('login foo@bar.com tests')
        msg = Project.command('login tests@tests.com tests')
        self.assertEqual(msg, 'Sorry, there is already someone logged in.')

    def test_given_a_new_user_logging_in_for_the_first_time__then_the_user_is_greeted_and_told_to_enter_new_password(self):
        msg = Project.command('login hello@world.com')
        self.assertEqual(msg, 'Welcome hello world. Please enter your new password:')

    def test_given_too_few_arguments_with_an_old_user__then_user_is_not_logged_in(self):
        msg = Project.command('login bar@foo.com')
        self.assertEqual(msg, INVALID_LOGIN_MESSAGE)
    
    def test_given_too_many_arguments__then_user_is_not_logged_in(self):
        msg = Project.command('login bar@foo.com tests hello')
        self.assertEqual(msg, 'Sorry, but that is too much information for one user')