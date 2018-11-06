import unittest
from tests.resources.TestDataAccess import TestDataAccess
from src.Account import Account
from src.CommandHandler import CommandHandler
from src.ErrorMessages import ErrorMessages


class LoginTest(unittest.TestCase):
    def setUp(self):
        self.db = TestDataAccess()
        Account.LoadEntity(self.db)
        self.ch = CommandHandler(self.db)

    def test_given_valid_login__then_user_is_logged_in(self):
        msg = self.ch.ProcessCommand('login dfudge@school.edu dfudge12')
        self.assertEqual(msg, 'Logged in as dfudge@school.edu')

    def test_given_valid_email_and_invalid_password__then_user_is_not_logged_in(self):
        msg = self.ch.ProcessCommand('login dfudge@school.edu test')
        self.assertEqual(msg, 'Invalid credentials')

    def test_given_invalid_email__then_user_is_not_logged_in(self):
        msg = self.ch.ProcessCommand('login invalid@user.com test')
        self.assertEqual(msg, 'Given email does not belong to an existing user')

    def test_given_a_new_user_logging_in_for_the_first_time__then_the_user_is_greeted_and_their_password_is_saved(self):
        msg = self.ch.ProcessCommand('login link@notzelda.com test')
        self.db.cur.execute('select * from accounts where act_email like ? and act_password like ?', ['link@notzelda.com', 'test'])
        self.assertIsNotNone(self.db.cur.fetchone())
        self.assertEqual(msg, 'Logged in as link@notzelda.com, your new password has been saved')

    def test_given_too_few_arguments_with_an_old_user__then_user_is_not_logged_in(self):
        msg = self.ch.ProcessCommand('login ta@one.com')
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
    
    def test_given_too_many_arguments__then_user_is_not_logged_in(self):
        msg = self.ch.ProcessCommand('login ta@one.com tests hello')
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
