import unittest
from tests.resources.TestDataAccess import TestDataAccess
from src.Account import Account
from src.Course import Course
from src.Lab import Lab
from src.CommandHandler import CommandHandler


class ViewingDataAsASupervisorTest(unittest.TestCase):
    def setUp(self):
        self.db = TestDataAccess()
        Account.LoadEntity(self.db)
        Course.LoadEntity(self.db)
        Lab.LoadEntity(self.db)
        self.ch = CommandHandler(self.db)
        self.ch.ProcessCommand('login dfudge@school.edu dfudge12')

    def test_viewing_specific_user_given_user_exists_then_user_info_is_displayed(self):
        msg = self.ch.ProcessCommand('view user asdf@yahoo.com')
        self.assertEqual(msg, 'asdf@yahoo.com | phil | smith | asdf123 | 999-424-4342 | 17 Oak | TA')

    def test_viewing_specific_user_given_user_does_not_exist_then_error_message_is_displayed(self):
        msg = self.ch.ProcessCommand('view user invalid@user.com')
        self.assertEqual(msg, 'Given email does not belong to an existing user')

    def test_viewing_specific_course_given_course_exist_then_course_is_displayed(self):
        msg = self.ch.ProcessCommand('view course "my course"')
        self.assertEqual(msg, '2 | my course | rock@uwm.edu')

    def test_viewing_specific_user_given_course_does_not_exist_then_error_message_is_displayed(self):
        msg = self.ch.ProcessCommand('view course "invalid course"')
        self.assertEqual(msg, 'Course does not exist')

    def test_viewing_specific_lab_given_course_exist_then_course_is_displayed(self):
        msg = self.ch.ProcessCommand('view lab 1')
        self.assertEqual(msg, '1 | Ayyy Lab | 1 | ta@gmail.com')

    def test_viewing_specific_course_given_no_lab_id_is_given_then_error_message_is_displayed(self):
        msg = self.ch.ProcessCommand('view lab "my course"')
        self.assertEqual(msg, 'Lab ID must be a non-negative integer')

    def test_viewing_specific_user_given_lab_does_not_exist_then_error_message_is_displayed(self):
        msg = self.ch.ProcessCommand('view lab 10')
        self.assertEqual(msg, 'Given lab does not exist')

    # def test_view_ta_list_then_tas_are_displayed(self):
    #     msg = Project.command('view tas')
    #     self.assertEqual(msg, view_ta_result_for_supervisor_string)

# Taking these out just for the time being seeing as we have tailored this sprint to Supervisors
# class ViewingDataAsAnInstructorTest(unittest.TestCase):
#     def setUp(self):
#         Project.command('login instructor@one.com test')
#
#     def test_viewing_specific_user_given_user_exists_then_user_public_info_is_displayed(self):
#         msg = Project.command('view user ta@one.com')
#         self.assertEquals(msg, json.dumps(view_ta_result_for_ta_or_instructor_json[0]))
#
#     def test_view_course_given_user_is_assigned_to_that_course_then_course_is_displayed(self):
#         msg = Project.command('view course \"course with ta\"')
#         self.assertEquals(msg, json.dumps(courses[0]))
#
#     def test_view_course_given_user_is_not_assigned_to_that_course_then_error_message_is_displayed(self):
#         msg = Project.command('view course \"course without ta\"')
#         self.assertEquals(msg, 'You are not assigned to this course')
#
#     def test_view_ta_list_then_tas_public_data_is_displayed(self):
#         msg = Project.command('view tas')
#         self.assertEquals(msg, view_ta_result_for_ta_or_instructor_string)
#
#
# class ViewingDataAsATaTest(unittest.TestCase):
#     def setUp(self):
#         Project.command('login ta@one.com test')
#
#     def test_viewing_specific_user_given_user_exists_then_user_public_info_is_displayed(self):
#         msg = Project.command('view user ta@two.com')
#         self.assertEquals(msg, json.dumps(view_ta_result_for_ta_or_instructor_json[1]))
#
#     def test_view_ta_list_then_tas_public_data_is_displayed(self):
#         msg = Project.command('view tas')
#         self.assertEquals(msg, view_ta_result_for_ta_or_instructor_string)
#
#     def test_view_course_then_error_message_is_displayed(self):
#         msg = Project.command('view course \"course with ta\"')
#         self.assertEquals(msg, 'You do not have permission to use this command')
