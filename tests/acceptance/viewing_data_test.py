import unittest
import json
import os
from src.project import Project

cwd = os.getcwd()
all_user_data = cwd + '/tests/resources/mock_users_data.json'
public_user_data = cwd + '/tests/resources/mock_users_public_data.json'
course_data = cwd + '/tests/resources/mock_course_data.json'
with open(all_user_data, 'r') as u_data:
    users_with_all_data = json.load(u_data)
with open(public_user_data, 'r') as u_public_data:
    users_public_data = json.load(u_public_data)
with open(course_data, 'r') as c_data:
    courses = json.load(c_data)

view_ta_result_for_supervisor_json = list(filter(lambda x: x['role'] == 'ta', users_with_all_data))
view_ta_result_for_supervisor_string = json.dumps(view_ta_result_for_supervisor_json)

view_ta_result_for_ta_or_instructor_json = list(filter(lambda x: x['role'] == 'ta', users_public_data))
view_ta_result_for_ta_or_instructor_string = json.dumps(view_ta_result_for_ta_or_instructor_json)


class ViewingDataAsASupervisorTest(unittest.TestCase):
    def setUp(self):
        Project.command('login supervisor@one.com test')

    def test_viewing_specific_user_given_user_exists_then_user_info_is_displayed(self):
        msg = Project.command('view user ta@one.com')
        self.assertEquals(msg, json.dumps(view_ta_result_for_supervisor_json[0]))

    def test_viewing_specific_user_given_user_does_not_exist_then_error_message_is_displayed(self):
        msg = Project.command('view user invalid@user.com')
        self.assertEquals(msg, 'User does not exist')

    def test_viewing_specific_course_given_course_exist_then_course_is_displayed(self):
        msg = Project.command('view course \"course with ta\"')
        self.assertEquals(msg, json.dumps(courses[0]))

    def test_viewing_specific_course_given_course_does_not_exist_then_error_message_is_displayed(self):
        msg = Project.command('view course \"invalid course\"')
        self.assertEquals(msg, 'Course does not exist')

    def test_view_ta_list_then_tas_are_displayed(self):
        msg = Project.command('view tas')
        self.assertEquals(msg, view_ta_result_for_supervisor_string)


class ViewingDataAsAnInstructorTest(unittest.TestCase):
    def setUp(self):
        Project.command('login instructor@one.com test')

    def test_viewing_specific_user_given_user_exists_then_user_public_info_is_displayed(self):
        msg = Project.command('view user ta@one.com')
        self.assertEquals(msg, json.dumps(view_ta_result_for_ta_or_instructor_json[0]))

    def test_view_course_given_user_is_assigned_to_that_course_then_course_is_displayed(self):
        msg = Project.command('view course \"course with ta\"')
        self.assertEquals(msg, json.dumps(courses[0]))

    def test_view_course_given_user_is_not_assigned_to_that_course_then_error_message_is_displayed(self):
        msg = Project.command('view course \"course without ta\"')
        self.assertEquals(msg, 'You are not assigned to this course')

    def test_view_ta_list_then_tas_public_data_is_displayed(self):
        msg = Project.command('view tas')
        self.assertEquals(msg, view_ta_result_for_ta_or_instructor_string)


class ViewingDataAsATaTest(unittest.TestCase):
    def setUp(self):
        Project.command('login ta@one.com test')

    def test_viewing_specific_user_given_user_exists_then_user_public_info_is_displayed(self):
        msg = Project.command('view user ta@two.com')
        self.assertEquals(msg, json.dumps(view_ta_result_for_ta_or_instructor_json[1]))

    def test_view_ta_list_then_tas_public_data_is_displayed(self):
        msg = Project.command('view tas')
        self.assertEquals(msg, view_ta_result_for_ta_or_instructor_string)

    def test_view_course_then_error_message_is_displayed(self):
        msg = Project.command('view course \"course with ta\"')
        self.assertEquals(msg, 'You do not have permission to use this command')
