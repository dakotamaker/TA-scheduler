import unittest
import json
import os
from src.project import Project

# Current user available:
cwd = os.getcwd()
user_data = cwd + '/tests/resources/mock_users_data.json'
course_data = cwd + '/tests/resources/mock_course_data.json'
with open(user_data, 'r') as u_data:
    users = json.load(u_data)


class LabsAndCoursesTest(unittest.TestCase):
    def setUp(self):
        Project.command('login supervisor@one.com test')
        with open(course_data, 'r') as c_data:
            self.courses = json.load(c_data)

    def test_creating_course_given_valid_name_then_course_is_created(self):
        Project.command('create course \"new course\"')
        self.assertEquals(len(self.courses), 4)

    def test_creating_course_given_name_that_exists_already_then_course_is_not_created(self):
        msg = Project.command('create course \"course with ta\"')
        self.assertEquals(msg, 'That course is already created')
        self.assertEquals(len(self.courses), 3)

    def test_creating_lab_given_valid_name_and_course_then_lab_is_created(self):
        Project.command('create lab \"course with ta\" \"lab2\"')
        self.assertEquals(len(self.courses[0]['labs']), 2)

    def test_creating_lab_given_name_that_exists_already_then_lab_is_not_created(self):
        msg = Project.command('create lab \"course with ta\" \"lab1\"')
        self.assertEquals(msg, 'That lab is already created for this course')
        self.assertEquals(len(self.courses[0]['labs']), 2)

    def test_creating_lab_given_course_name_that_does_not_exist_then_lab_is_not_created(self):
        msg = Project.command('create lab \"invalid course\" \"lab1\"')
        self.assertEquals(msg, 'That course does not exist yet')

    def test_creating_course_given_no_third_argument_in_quotes_in_the_command_then_error_message_is_thrown(self):
        msg = Project.command('create course new')
        self.assertEquals(msg, 'Invalid arguments')

    def test_creating_lab_given_no_third_argument_in_quotes_in_the_command_then_error_message_is_thrown(self):
        msg = Project.command('create lab new \"lab1\"')
        self.assertEquals(msg, 'Invalid arguments')

    def test_creating_course_given_no_fourth_argument_in_quotes_in_the_command_then_error_message_is_thrown(self):
        msg = Project.command('create lab \"new\" lab1')
        self.assertEquals(msg, 'Invalid arguments')

    def test_assigning_a_course_to_an_instructor_given_course_and_instructor_exist_then_instructor_is_assigned(self):
        self.assertEquals(self.courses[0]['instructor'], 'instructor@one.com')
        Project.command('assign course \"course with ta\" instructor@two.com')
        self.assertEquals(self.courses[0]['instructor'], 'instructor@two.com')

    def test_assigning_a_course_to_an_instructor_given_course_does_not_exist_then_error_is_displayed(self):
        msg = Project.command('assign course \"invalid course\" instructor@two.com')
        self.assertEquals(msg, 'That course does not exist')

    def test_assigning_a_course_to_an_instructor_given_instructor_does_not_exist_then_error_is_displayed(self):
        msg = Project.command('assign course \"course with ta\" invalid@user.com')
        self.assertEquals(msg, 'That user does not exist')

    def test_assigning_a_course_to_a_ta_given_ta_and_course_exist_then_ta_is_assigned(self):
        self.assertEquals(len(self.courses[1]['tas']), 0)
        Project.command('assign course \"course with no ta\" ta@one.com')
        self.assertEquals(len(self.courses[1]['tas']), 1)

    def test_assigning_a_lab_to_a_ta_given_ta_and_lab_exist_then_ta_is_assigned(self):
        Project.command('assign lab \"course with ta\" \"lab1\" ta@two.com')
        self.assertEquals(len(self.courses[1]['labs'][0]['ta']), 'ta@two.com')

    def test_assigning_a_lab_to_a_ta_given_ta_does_not_exist_then_error_is_displayed(self):
        msg = Project.command('assign lab \"course with ta\" \"lab1\" invalid@ta.com')
        self.assertEquals(msg, "This user does not exist")

    def test_assigning_a_lab_to_a_ta_given_lab_does_not_exist_then_error_is_displayed(self):
        msg = Project.command('assign lab \"course with no ta\" \"invalid lab\" ta@one.com')
        self.assertEquals(msg, "This lab does not exist")

    def test_assigning_a_course_to_an_admin_then_error_is_displayed(self):
        msg = Project.command('assign course \"course with ta\" admin@one.com')
        self.assertEquals(msg, 'Only TAs and instructors can be assigned to courses')

    def test_assigning_a_lab_to_an_admin_then_error_is_displayed(self):
        msg = Project.command('assign lab \"course with ta\" \"lab1\" admin@one.com')
        self.assertEquals(msg, 'Only TAs can be assigned to labs')

    def test_assigning_a_lab_to_an_instructor_then_error_is_displayed(self):
        msg = Project.command('assign lab \"course with ta\" \"lab1\" instructor@one.com')
        self.assertEquals(msg, 'Only TAs can be assigned to labs')

