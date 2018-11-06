import unittest
from tests.resources.TestDataAccess import TestDataAccess
from src.Account import Account
from src.CommandHandler import CommandHandler


class UsersAsASupervisorTest(unittest.TestCase):
    def setUp(self):
        self.db = TestDataAccess()
        Account.LoadEntity(self.db)
        self.ch = CommandHandler(self.db)
        self.ch.ProcessCommand('login dfudge@school.edu dfudge12')

    def test_creating_a_user_given_all_valid_arguments_then_user_is_created(self):
        self.ch.ProcessCommand('create user new@test.com new test-user ta 1112223333 \"test st\"')
        self.db.cur.execute('select * from accounts where act_email like ?', ['new@test.com'])
        self.assertIsNotNone(self.db.cur.fetchone())

    def test_creating_a_user_given_user_already_exits_then_no_new_user_is_created(self):
        self.ch.ProcessCommand('create user new@test.com new test-user ta \"test st\"')
        self.db.cur.execute('select * from accounts where act_email like ?', ['new@test.com'])
        self.assertIsNone(self.db.cur.fetchone())

    def test_creating_a_user_given_too_few_arguments(self):
        self.ch.ProcessCommand('create user new@test.com new test-user ta \"test st\"')
        self.db.cur.execute('select * from accounts where act_email like ?', ['new@test.com'])
        self.assertIsNone(self.db.cur.fetchone())

    def test_creating_a_user_given_too_many_arguments(self):
        self.ch.ProcessCommand('create user new@test.com new test-user ta 1112223333 \"test st\" too-many-arguments')
        self.db.cur.execute('select * from accounts where act_email like ?', ['new@test.com'])
        self.assertIsNone(self.db.cur.fetchone())

    # Commenting out since these won't work for now since we don't have any delete logic
    # def test_delete_a_user_given_user_exists_then_user_is_removed(self):
    #     self.assertEquals(len(self.users), 7)
    #     Project.command('delete user ta@one.com')
    #     self.assertEquals(len(self.users), 6)

    # def test_delete_a_user_given_user_does_not_exist_then_error_is_displayed(self):
    #     msg = Project.command('delete user invalid@user.com')
    #     self.assertEquals(msg, 'That user does not exist')

    def test_editing_another_user_given_valid_arguments_then_user_is_edited(self):
        Project.command('edit user ta@one.com firstName:\"newName\"')
        self.assertEquals(self.users[0]['firstName'], 'newName')

    def test_editing_another_user_given_attribute_that_does_not_exist_then_error_is_displayed(self):
        msg = Project.command('edit user ta@one.com invalid:\"newName\"')
        self.assertEquals(msg, 'That attribute does not exist')


class UsersAsAnInstructorTest(unittest.TestCase):
    def setUp(self):
        db = TestDataAccess()
        Account.LoadEntity(db)
        ch = CommandHandler(db)
        ch.ProcessCommand('login asdf@yahoo.com asdf123')

    def test_editing_own_information_given_valid_arguments_then_user_info_is_edited(self):
        Project.command('edit firstName:\"newName\"')
        self.assertEquals(self.users[4]['firstName'], 'newName')

    def test_editing_own_information_given_invalid_arguments_then_error_is_displayed(self):
        msg = Project.command('edit invalid:\"newName\"')
        self.assertEquals(msg, 'That attribute does not exist')

    def test_try_editing_other_users_info_then_error_is_displayed(self):
        msg = Project.command('edit user ta@one.com firstName:\"newName\"')
        self.assertEquals(msg, 'You do not have permission to edit another user')
