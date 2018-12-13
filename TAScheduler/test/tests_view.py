from django.test import TestCase
from ..models import Account
from ..models import Course
from ..models import Lab
from ..domain.CommandHandler import CommandHandler

ALL_TA_INFO_STRING = 'Account email: test@ta.com\nFirst name: test\nLast name: ta\nPhone number: 1112223333\nAddress: 123 test dr\nOffice hours: 10-11\nOffice Location: 123 EMS'
PUBLIC_TA_INFO_STRING = 'Account email: test@ta.com\nFirst name: test\nLast name: ta\nOffice hours: 10-11\nOffice Location: 123 EMS'


class UserAsSupervisor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.admin = Account.objects.create(act_email='super@email.com', role_id=4)
        self.ta = Account.objects.create(act_email='test@ta.com', act_fname='test', act_lname='ta', act_phone='1112223333',
                                         act_address='123 test dr', act_officehours='10-11', act_officelocation='123 EMS',
                                         role_id=1)
        self.ch.currentUser = self.admin

    def test_view_given_too_many_arguments_expect_error(self):
        msg = self.ch.ProcessCommand('view user test@ta.com blah')
        self.assertEqual(msg, 'Invalid number of arguments')

    def test_view_given_too_few_arguments_expect_error(self):
        msg = self.ch.ProcessCommand('view user')
        self.assertEqual(msg, 'Invalid number of arguments')

    def test_view_user_get_all_user_info(self):
        msg = self.ch.ProcessCommand('view user test@ta.com')
        self.assertEqual(msg, ALL_TA_INFO_STRING)


class UserAsAdmin(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.admin = Account.objects.create(act_email='super@email.com', role_id=3)
        self.ta = Account.objects.create(act_email='test@ta.com', act_fname='test', act_lname='ta', act_phone='1112223333',
                                         act_address='123 test dr', act_officehours='10-11', act_officelocation='123 EMS',
                                         role_id=1)
        self.ch.currentUser = self.admin

    def test_view_user_get_all_user_info(self):
        msg = self.ch.ProcessCommand('view user test@ta.com')
        self.assertEqual(msg, ALL_TA_INFO_STRING)


class UserAsInstructor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.admin = Account.objects.create(act_email='super@email.com', role_id=2)
        self.ta = Account.objects.create(act_email='test@ta.com', act_fname='test', act_lname='ta', act_phone='1112223333',
                                         act_address='123 test dr', act_officehours='10-11', act_officelocation='123 EMS',
                                         role_id=1)
        self.ch.currentUser = self.admin

    def test_view_user_get_all_public_user_info(self):
        msg = self.ch.ProcessCommand('view user test@ta.com')
        self.assertEqual(msg, PUBLIC_TA_INFO_STRING)


class UserAsTA(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.admin = Account.objects.create(act_email='super@email.com', role_id=1)
        self.ta = Account.objects.create(act_email='test@ta.com', act_fname='test', act_lname='ta', act_phone='1112223333',
                                         act_address='123 test dr', act_officehours='10-11', act_officelocation='123 EMS',
                                         role_id=1)
        self.ch.currentUser = self.admin

    def test_view_user_get_all_public_user_info(self):
        msg = self.ch.ProcessCommand('view user test@ta.com')
        self.assertEqual(msg, PUBLIC_TA_INFO_STRING)


class CourseAsSupervisor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.super = Account.objects.create(act_email='super@email.com', role_id=4)
        self.ta1 = Account.objects.create(act_email='ta1@email.com', role_id=1)
        self.ta2 = Account.objects.create(act_email='ta2@email.com', role_id=1)
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)
        self.course = Course.objects.create(course_name='course1', instructor=self.instructor)
        self.ch.currentUser = self.super
        self.ch.ProcessCommand('assign course ta "course1" ta1@email.com')
        self.ch.ProcessCommand('assign course ta "course1" ta2@email.com')

    def test_viewing_course_and_course_info_is_returned(self):
        msg = self.ch.ProcessCommand('view course course1')
        self.assertIn(msg, 'Course name: course1\nInstructor: instructor@email.com\nTAs: ta1@email.com, ta2@email.com.')

    def test_viewing_course_given_course_does_not_exist_then_error_is_returned(self):
        msg = self.ch.ProcessCommand('view course course2')
        self.assertEqual(msg, 'Course does not exist')

    def test_viewing_course_given_too_many_arguments_then_error_is_returned(self):
        msg = self.ch.ProcessCommand('view course course1 test')
        self.assertEqual(msg, 'Invalid number of arguments')

    def test_viewing_course_given_too_few_arguments_then_error_is_returned(self):
        msg = self.ch.ProcessCommand('view course')
        self.assertEqual(msg, 'Invalid number of arguments')


class CourseAsAdmin(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
        self.ta1 = Account.objects.create(act_email='ta1@email.com', role_id=1)
        self.ta2 = Account.objects.create(act_email='ta2@email.com', role_id=1)
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)
        self.course = Course.objects.create(course_name='course1', instructor=self.instructor)
        self.ch.currentUser = self.admin
        self.ch.ProcessCommand('assign course ta "course1" ta1@email.com')
        self.ch.ProcessCommand('assign course ta "course1" ta2@email.com')

    def test_viewing_course_and_course_info_is_returned(self):
        msg = self.ch.ProcessCommand('view course course1')
        self.assertIn(msg, 'Course name: course1\nInstructor: instructor@email.com\nTAs: ta1@email.com, ta2@email.com.')

    def test_viewing_course_given_course_does_not_exist_then_error_is_returned(self):
        msg = self.ch.ProcessCommand('view course course2')
        self.assertEqual(msg, 'Course does not exist')

    def test_viewing_course_given_too_many_arguments_then_error_is_returned(self):
        msg = self.ch.ProcessCommand('view course course1 test')
        self.assertEqual(msg, 'Invalid number of arguments')

    def test_viewing_course_given_too_few_arguments_then_error_is_returned(self):
        msg = self.ch.ProcessCommand('view course')
        self.assertEqual(msg, 'Invalid number of arguments')

class CourseAsInstructor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta1 = Account.objects.create(act_email='ta1@email.com', role_id=1)
        self.ta2 = Account.objects.create(act_email='ta2@email.com', role_id=1)
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)
        self.course = Course.objects.create(course_name='course1', instructor=self.instructor)
        self.ch.currentUser = self.instructor
        self.ch.ProcessCommand('assign course ta "course1" ta1@email.com')
        self.ch.ProcessCommand('assign course ta "course1" ta2@email.com')

    def test_viewing_course_and_course_info_is_returned(self):
        msg = self.ch.ProcessCommand('view course course1')
        self.assertIn(msg, 'Course name: course1\nInstructor: instructor@email.com\nTAs: ta1@email.com, ta2@email.com.')

    def test_viewing_course_given_course_does_not_exist_then_error_is_returned(self):
        msg = self.ch.ProcessCommand('view course course2')
        self.assertEqual(msg, 'Course does not exist')

    def test_viewing_course_given_too_many_arguments_then_error_is_returned(self):
        msg = self.ch.ProcessCommand('view course course1 test')
        self.assertEqual(msg, 'Invalid number of arguments')

    def test_viewing_course_given_too_few_arguments_then_error_is_returned(self):
        msg = self.ch.ProcessCommand('view course')
        self.assertEqual(msg, 'Invalid number of arguments')


class CourseAsTA(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)
        self.course = Course.objects.create(course_name='course1', instructor=self.instructor)
        self.ch.currentUser = self.ta

    def test_viewing_course_and_course_info_is_returned(self):
        msg = self.ch.ProcessCommand('view course course1')
        self.assertEqual(msg, 'Must be logged in as an Instructor, Administrator, or a Supervisor')


class LabAsSupervisor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.super = Account.objects.create(act_email='super@email.com', role_id=4)
        self.ta1 = Account.objects.create(act_email='ta1@email.com', role_id=1)
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)
        self.course1 = Course.objects.create(course_name='course1', instructor=self.instructor)
        self.course2 = Course.objects.create(course_name='course2', instructor=self.instructor)
        self.ch.currentUser = self.super
        self.lab1_c1 = Lab.objects.create(lab_name="lab1", course=self.course1, ta=self.ta1)
        self.lab1_c2 = Lab.objects.create(lab_name="lab1", course=self.course2, ta=self.ta1)

    def test_viewing_lab_and_lab_info_is_returned(self):
        msg = self.ch.ProcessCommand('view lab course1 lab1')
        self.assertIn(msg, 'Lab name: lab1\nCourse: course1\nTA: ta1@email.com')

    def test_viewing_lab_with_same_lab_name_but_different_course_then_lab_info_is_returned(self):
        msg = self.ch.ProcessCommand('view lab course2 lab1')
        self.assertIn(msg, 'Lab name: lab1\nCourse: course2\nTA: ta1@email.com')

    def test_viewing_lab_with_course_that_does_not_exist_then_error_occurs(self):
        msg = self.ch.ProcessCommand('view lab course3 lab1')
        self.assertIn(msg, 'Course does not exist')

    def test_viewing_lab_with_lab_that_does_not_exist_then_error_occurs(self):
        msg = self.ch.ProcessCommand('view lab course1 lab2')
        self.assertIn(msg, 'Lab does not exist')

    def test_viewing_lab_given_too_many_arguments_then_error_is_returned(self):
        msg = self.ch.ProcessCommand('view lab course1 lab1 test')
        self.assertEqual(msg, 'Invalid number of arguments')

    def test_viewing_lab_given_too_few_arguments_then_error_is_returned(self):
        msg = self.ch.ProcessCommand('view lab course1')
        self.assertEqual(msg, 'Invalid number of arguments')


class LabAsAdmin(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=4)
        self.ta1 = Account.objects.create(act_email='ta1@email.com', role_id=1)
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)
        self.course1 = Course.objects.create(course_name='course1', instructor=self.instructor)
        self.course2 = Course.objects.create(course_name='course2', instructor=self.instructor)
        self.ch.currentUser = self.admin
        self.lab1_c1 = Lab.objects.create(lab_name="lab1", course=self.course1, ta=self.ta1)
        self.lab1_c2 = Lab.objects.create(lab_name="lab1", course=self.course2, ta=self.ta1)

    def test_viewing_lab_and_lab_info_is_returned(self):
        msg = self.ch.ProcessCommand('view lab course1 lab1')
        self.assertIn(msg, 'Lab name: lab1\nCourse: course1\nTA: ta1@email.com')

    def test_viewing_lab_with_same_lab_name_but_different_course_then_lab_info_is_returned(self):
        msg = self.ch.ProcessCommand('view lab course2 lab1')
        self.assertIn(msg, 'Lab name: lab1\nCourse: course2\nTA: ta1@email.com')

    def test_viewing_lab_with_course_that_does_not_exist_then_error_occurs(self):
        msg = self.ch.ProcessCommand('view lab course3 lab1')
        self.assertIn(msg, 'Course does not exist')

    def test_viewing_lab_with_lab_that_does_not_exist_then_error_occurs(self):
        msg = self.ch.ProcessCommand('view lab course1 lab2')
        self.assertIn(msg, 'Lab does not exist')

    def test_viewing_lab_given_too_many_arguments_then_error_is_returned(self):
        msg = self.ch.ProcessCommand('view lab course1 lab1 test')
        self.assertEqual(msg, 'Invalid number of arguments')

    def test_viewing_lab_given_too_few_arguments_then_error_is_returned(self):
        msg = self.ch.ProcessCommand('view lab course1')
        self.assertEqual(msg, 'Invalid number of arguments')


class LabAsInstructor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.instruc = Account.objects.create(act_email='instruc@email.com', role_id=4)
        self.ta1 = Account.objects.create(act_email='ta1@email.com', role_id=1)
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)
        self.course1 = Course.objects.create(course_name='course1', instructor=self.instructor)
        self.course2 = Course.objects.create(course_name='course2', instructor=self.instructor)
        self.ch.currentUser = self.instruc
        self.lab1_c1 = Lab.objects.create(lab_name="lab1", course=self.course1, ta=self.ta1)
        self.lab1_c2 = Lab.objects.create(lab_name="lab1", course=self.course2, ta=self.ta1)

    def test_viewing_lab_and_lab_info_is_returned(self):
        msg = self.ch.ProcessCommand('view lab course1 lab1')
        self.assertIn(msg, 'Lab name: lab1\nCourse: course1\nTA: ta1@email.com')

    def test_viewing_lab_with_same_lab_name_but_different_course_then_lab_info_is_returned(self):
        msg = self.ch.ProcessCommand('view lab course2 lab1')
        self.assertIn(msg, 'Lab name: lab1\nCourse: course2\nTA: ta1@email.com')

    def test_viewing_lab_with_course_that_does_not_exist_then_error_occurs(self):
        msg = self.ch.ProcessCommand('view lab course3 lab1')
        self.assertIn(msg, 'Course does not exist')

    def test_viewing_lab_with_lab_that_does_not_exist_then_error_occurs(self):
        msg = self.ch.ProcessCommand('view lab course1 lab2')
        self.assertIn(msg, 'Lab does not exist')

    def test_viewing_lab_given_too_many_arguments_then_error_is_returned(self):
        msg = self.ch.ProcessCommand('view lab course1 lab1 test')
        self.assertEqual(msg, 'Invalid number of arguments')

    def test_viewing_lab_given_too_few_arguments_then_error_is_returned(self):
        msg = self.ch.ProcessCommand('view lab course1')
        self.assertEqual(msg, 'Invalid number of arguments')


class LabAsTa(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=4)
        self.ta1 = Account.objects.create(act_email='ta1@email.com', role_id=1)
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)
        self.course1 = Course.objects.create(course_name='course1', instructor=self.instructor)
        self.course2 = Course.objects.create(course_name='course2', instructor=self.instructor)
        self.ch.currentUser = self.ta
        self.lab1_c1 = Lab.objects.create(lab_name="lab1", course=self.course1, ta=self.ta1)
        self.lab1_c2 = Lab.objects.create(lab_name="lab1", course=self.course2, ta=self.ta1)

    def test_viewing_lab_and_lab_info_is_returned(self):
        msg = self.ch.ProcessCommand('view lab course1 lab1')
        self.assertIn(msg, 'Lab name: lab1\nCourse: course1\nTA: ta1@email.com')

    def test_viewing_lab_with_same_lab_name_but_different_course_then_lab_info_is_returned(self):
        msg = self.ch.ProcessCommand('view lab course2 lab1')
        self.assertIn(msg, 'Lab name: lab1\nCourse: course2\nTA: ta1@email.com')

    def test_viewing_lab_with_course_that_does_not_exist_then_error_occurs(self):
        msg = self.ch.ProcessCommand('view lab course3 lab1')
        self.assertIn(msg, 'Course does not exist')

    def test_viewing_lab_with_lab_that_does_not_exist_then_error_occurs(self):
        msg = self.ch.ProcessCommand('view lab course1 lab2')
        self.assertIn(msg, 'Lab does not exist')

    def test_viewing_lab_given_too_many_arguments_then_error_is_returned(self):
        msg = self.ch.ProcessCommand('view lab course1 lab1 test')
        self.assertEqual(msg, 'Invalid number of arguments')

    def test_viewing_lab_given_too_few_arguments_then_error_is_returned(self):
        msg = self.ch.ProcessCommand('view lab course1')
        self.assertEqual(msg, 'Invalid number of arguments')


class ListTAsTestCase(TestCase):
    def setUp(self):
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)

        self.ta1 = Account.objects.create(act_email='ta1@email.com', role_id=1, act_password='1111')
        self.ta2 = Account.objects.create(act_email='ta2@email.com', role_id=1)
        self.ta3 = Account.objects.create(act_email='ta3@email.com', role_id=1)
        self.ta4 = Account.objects.create(act_email='ta4@email.com', role_id=1)

        self.course1 = Course.objects.create(course_id='535', course_name='Algorithms', instructor=self.instructor)
        self.course1.tas.set([self.ta1, self.ta3])
        self.lab1 = Lab.objects.create(lab_id='1', lab_name='AlgoLab', course=self.course1, ta=self.ta1)

        self.course2 = Course.objects.create(course_id='557', course_name='Databases', instructor=self.instructor)
        self.course2.tas.set([self.ta2, self.ta3])
        self.lab2 = Lab.objects.create(lab_id='2', lab_name='DataLab', course=self.course2, ta=self.ta2)

        self.ch = CommandHandler()

    def test_without_valid_login__then_list_fails(self):
        msg = self.ch.ProcessCommand("list tas")
        self.assertEqual(msg, 'Must be logged in to access TA list.')

    def test_with_loggedInUser__then_list_succeeds(self):
        self.ch.ProcessCommand("login ta1@email.com 1111")
        msg = self.ch.ProcessCommand("list tas")
        self.assertIn(msg, 'List TAs: \n : Algorithms\tAlgoLab\t\n : Databases\tDataLab\t\n : Algorithms\tDatabases\t\n : ')