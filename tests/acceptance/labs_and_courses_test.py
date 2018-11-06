import unittest
from tests.resources.TestDataAccess import TestDataAccess
from src.Account import Account
from src.Course import Course
from src.Lab import Lab
from src.CommandHandler import CommandHandler
from src.ErrorMessages import ErrorMessages


class LabsAndCoursesTest(unittest.TestCase):
    def setUp(self):
        self.db = TestDataAccess()
        Account.LoadEntity(self.db)
        Course.LoadEntity(self.db)
        Lab.LoadEntity(self.db)
        self.ch = CommandHandler(self.db)
        self.ch.ProcessCommand('login dfudge@school.edu dfudge12')

    def test_creating_course_given_valid_name_then_course_is_created(self):
        self.ch.ProcessCommand('create course "new course"')
        self.db.cur.execute('select * from courses where course_name like ?', ['new course'])
        self.assertIsNotNone(self.db.cur.fetchone())

    def test_creating_course_given_name_that_exists_already_then_course_is_not_created(self):
        msg = self.ch.ProcessCommand('create course "my course"')
        self.assertEqual(msg, 'Course already exists.')

    def test_creating_course_given_too_many_arguments_then_error_is_displayed(self):
        msg = self.ch.ProcessCommand('create course "my course" test')
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)

    def test_creating_course_given_too_few_arguments_then_error_is_displayed(self):
        msg = self.ch.ProcessCommand('create course')
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)

    def test_assigning_a_course_to_an_instructor_given_course_and_instructor_exist_then_instructor_is_assigned(self):
        self.ch.ProcessCommand('assign course "my course" email@gmail.com')
        self.db.cur.execute('select * from courses where course_name like ? and instructor_email like ?', ['my course', 'email@gmail.com'])
        self.assertIsNotNone(self.db.cur.fetchone())

    def test_assigning_a_course_to_an_instructor_given_course_does_not_exist_then_error_is_displayed(self):
        msg = self.ch.ProcessCommand('assign course "invalid course" email@gmail.com')
        self.assertEqual(msg, 'This course does not exist.')

    def test_assigning_a_course_to_an_instructor_given_instructor_does_not_exist_then_error_is_displayed(self):
        msg = self.ch.ProcessCommand('assign course "my course" invalid@user.com')
        self.assertEqual(msg, 'This user does not exist.')

    def test_assigning_course_given_too_many_arguments_then_error_is_displayed(self):
        msg = self.ch.ProcessCommand('assign course "my course" invalid@user.com test')
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)

    def test_assigning_course_given_too_few_arguments_then_error_is_displayed(self):
        msg = self.ch.ProcessCommand('assign course')
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)

    # No logic for creating labs yet, so leaving that out for now
    # def test_creating_lab_given_valid_name_and_course_then_lab_is_created(self):
    #     Project.command('create lab "course with ta" "lab2"')
    #     self.assertEquals(len(self.courses[0]['labs']), 2)
    #
    # def test_creating_lab_given_name_that_exists_already_then_lab_is_not_created(self):
    #     msg = Project.command('create lab "course with ta" "lab1"')
    #     self.assertEquals(msg, 'That lab is already created for this course')
    #     self.assertEquals(len(self.courses[0]['labs']), 2)
    #
    # def test_creating_lab_given_course_name_that_does_not_exist_then_lab_is_not_created(self):
    #     msg = Project.command('create lab "invalid course" "lab1"')
    #     self.assertEquals(msg, 'That course does not exist yet')
    #
    # def test_creating_course_given_no_third_argument_in_quotes_in_the_command_then_error_message_is_thrown(self):
    #     msg = Project.command('create course new')
    #     self.assertEquals(msg, 'Invalid arguments')
    #
    # def test_creating_lab_given_no_third_argument_in_quotes_in_the_command_then_error_message_is_thrown(self):
    #     msg = Project.command('create lab new "lab1"')
    #     self.assertEquals(msg, 'Invalid arguments')
    #
    # def test_creating_lab_given_no_fourth_argument_in_quotes_in_the_command_then_error_message_is_thrown(self):
    #     msg = Project.command('create lab "new" lab1')
    #     self.assertEquals(msg, 'Invalid arguments')

    # def test_assigning_a_lab_to_a_ta_given_ta_and_lab_exist_then_ta_is_assigned(self):
    #     Project.command('assign lab "course with ta" "lab1" ta@two.com')
    #     self.assertEquals(len(self.courses[1]['labs'][0]['ta']), 'ta@two.com')
    #
    # def test_assigning_a_lab_to_a_ta_given_ta_does_not_exist_then_error_is_displayed(self):
    #     msg = Project.command('assign lab "course with ta" "lab1" invalid@ta.com')
    #     self.assertEquals(msg, "This user does not exist")
    #
    # def test_assigning_a_lab_to_a_ta_given_lab_does_not_exist_then_error_is_displayed(self):
    #     msg = Project.command('assign lab "course with no ta" "invalid lab" ta@one.com')
    #     self.assertEquals(msg, "This lab does not exist")
    # def test_assigning_a_lab_to_an_admin_then_error_is_displayed(self):
    #     msg = Project.command('assign lab "course with ta" "lab1" admin@one.com')
    #     self.assertEquals(msg, 'Only TAs can be assigned to labs')
    # def test_assigning_a_lab_to_an_instructor_then_error_is_displayed(self):
    #     msg = Project.command('assign lab "course with ta" "lab1" instructor@one.com')
    #     self.assertEquals(msg, 'Only TAs can be assigned to labs')

