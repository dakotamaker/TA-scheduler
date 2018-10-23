import unittest
import json
import os
from src.project import Project

cwd = os.getcwd()
user_data = cwd + '/tests/resources/mock_users_data.json'


class UsersAsASupervisorTest(unittest.TestCase):
    def setUp(self):
        Project.command('login supervisor@one.com test')
        with open(user_data, 'r') as u_data:
            self.users = json.load(u_data)

    def test_creating_a_user_given_all_valid_arguments_then_user_is_created(self):
        self.assertEquals(len(self.users), 7)
        Project.command('create user new@test.com new test-user ta 1112223333 \"test st\"')
        self.assertEquals(len(self.users), 8)

    def test_creating_a_user_given_address_is_missing_quotes_then_value_error_is_thrown(self):
        with self.assertRaises(ValueError):
            Project.command('create user new@test.com new test-user ta 111-222-3333 test')

    def test_creating_a_user_given_phone_number_has_special_characters_then_value_error_is_thrown(self):
        with self.assertRaises(ValueError):
            Project.command('create user new@test.com new test-user ta 111-222-3333 \"test st\"')

    def test_creating_a_user_given_too_few_arguments(self):
        msg = Project.command('create user new@test.com new test-user ta \"test st\"')
        self.assertEquals(msg, 'Too few arguments to create a user')

    def test_creating_a_user_given_too_many_arguments(self):
        msg = Project.command('create user new@test.com new test-user ta 1112223333 \"test st\" too-many-arguments')
        self.assertEquals(msg, 'Too many arguments to create a user')

    def test_delete_a_user_given_user_exists_then_user_is_removed(self):
        self.assertEquals(len(self.users), 7)
        Project.command('delete user ta@one.com')
        self.assertEquals(len(self.users), 6)

    def test_delete_a_user_given_user_does_not_exist_then_error_is_displayed(self):
        msg = Project.command('delete user invalid@user.com')
        self.assertEquals(msg, 'That user does not exist')

    def test_editing_another_user_given_valid_arguments_then_user_is_edited(self):
        Project.command('edit user ta@one.com firstName:\"newName\"')
        self.assertEquals(self.users[0]['firstName'], 'newName')

    def test_editing_another_user_given_attribute_that_does_not_exist_then_error_is_displayed(self):
        msg = Project.command('edit user ta@one.com invalid:\"newName\"')
        self.assertEquals(msg, 'That attribute does not exist')


class UsersAsAnInstructorTest(unittest.TestCase):
    def setUp(self):
        Project.command('login instructor@one.com test')
        with open(user_data, 'r') as u_data:
            self.users = json.load(u_data)

    def test_editing_own_information_given_valid_arguments_then_user_info_is_edited(self):
        Project.command('edit firstName:\"newName\"')
        self.assertEquals(self.users[4]['firstName'], 'newName')

    def test_editing_own_information_given_invalid_arguments_then_error_is_displayed(self):
        msg = Project.command('edit invalid:\"newName\"')
        self.assertEquals(msg, 'That attribute does not exist')

    def test_try_editing_other_users_info_then_error_is_displayed(self):
        msg = Project.command('edit user ta@one.com firstName:\"newName\"')
        self.assertEquals(msg, 'You do not have permission to edit another user')
