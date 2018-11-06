import unittest
from tests.resources.TestDataAccess import TestDataAccess
from src.Account import Account
from src.CommandHandler import CommandHandler
from src.ErrorMessages import ErrorMessages


class UsersAsASupervisorTest(unittest.TestCase):
    def setUp(self):
        self.db = TestDataAccess()
        Account.LoadEntity(self.db)
        self.ch = CommandHandler(self.db)
        self.ch.ProcessCommand('login dfudge@school.edu dfudge12')

    def test_creating_a_user_given_all_valid_arguments_then_user_is_created(self):
        self.ch.ProcessCommand('create user new@test.com new user 0 1112223333 \"test st\"')
        self.db.cur.execute('select * from accounts where act_email like ?', ['new@test.com'])
        self.assertIsNotNone(self.db.cur.fetchone())

    def test_creating_a_user_given_user_already_exits_then_no_new_user_is_created(self):
        msg = self.ch.ProcessCommand('create user dfudge@school.edu new user 0 1112223333 \"test st\"')
        self.assertEqual(msg, 'User already exists.')

    def test_creating_a_user_given_too_few_arguments_then_error_is_displayed(self):
        msg = self.ch.ProcessCommand('create user new@test.com new test-user ta \"test st\"')
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)

    def test_creating_a_user_given_too_many_arguments_then_error_is_displayed(self):
        msg = self.ch.ProcessCommand('create user new@test.com new test-user ta 1112223333 \"test st\" too-many-arguments')
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)

    def test_deleting_a_user_given_user_exists_then_user_is_removed(self):
        msg = self.ch.ProcessCommand('delete user asdf@yahoo.com')
        self.db.cur.execute('select * from accounts where act_email like ?', ['asdf@yahoo.com'])
        self.assertIsNone(self.db.cur.fetchone())
        self.assertEqual(msg, 'Removed asdf@yahoo.com')

    def test_deleting_a_user_given_user_does_not_exist_then_error_is_displayed(self):
        msg = self.ch.ProcessCommand('delete user invalid@user.com')
        self.assertEqual(msg, 'Given email does not belong to an existing user')

    def test_deleting_a_user_given_too_many_arguments_then_error_is_displayed(self):
        msg = self.ch.ProcessCommand('delete user invalid@user.com test')
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)

    def test_deleting_a_user_given_too_few_arguments_then_error_is_displayed(self):
        msg = self.ch.ProcessCommand('delete user')
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)

    def test_editing_another_user_given_valid_arguments_then_user_is_edited(self):
        self.ch.ProcessCommand('edit user asdf@yahoo.com act_password:test')
        self.db.cur.execute('select * from accounts where act_email like ? and act_password like ?', ['asdf@yahoo.com', 'test'])
        self.assertIsNotNone(self.db.cur.fetchone())

    def test_editing_another_user_given_attribute_that_does_not_exist_then_error_is_displayed(self):
        msg = self.ch.ProcessCommand('edit user invalid@email.com act_password:test')
        self.db.cur.execute('select * from accounts where act_email like ? and act_password like ?', ['asdf@yahoo.com', 'test'])
        self.assertIsNone(self.db.cur.fetchone())
        self.assertEqual(msg, 'invalid@email.com does not exist')

    def test_editing_own_information_given_valid_arguments_then_user_info_is_edited(self):
        self.ch.ProcessCommand('edit act_password:test')
        self.db.cur.execute('select * from accounts where act_email like ? and act_password like ?', ['dfudge@school.edu', 'test'])
        self.assertIsNotNone(self.db.cur.fetchone())

    def test_editing_own_information_given_too_many_arguments_then_user_is_not_edited(self):
        msg = self.ch.ProcessCommand('edit act_password:test hello')
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)

class UsersAsAnInstructorTest(unittest.TestCase):
    def setUp(self):
        self.db = TestDataAccess()
        Account.LoadEntity(self.db)
        self.ch = CommandHandler(self.db)
        self.ch.ProcessCommand('login asdf@yahoo.com asdf123')

    def test_try_editing_other_users_info_then_user_is_not_updated(self):
        self.ch.ProcessCommand('edit user dfudge12@school.com act_password:test')
        self.db.cur.execute('select * from accounts where act_email like ? and act_password like ?', ['dfudge12@school.com', 'test'])
        self.assertIsNone(self.db.cur.fetchone())
