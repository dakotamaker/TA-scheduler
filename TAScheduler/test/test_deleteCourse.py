from django.test import TestCase
from ..models import Account
from ..models import Course
from ..domain.CommandHandler import CommandHandler


class UserAsSupervisor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.admin = Account.objects.create(act_email='super@email.com', role_id=4)
        self.ch.currentUser = self.admin
        Course.objects.create(course_id='535', course_name='Algorithms', instructor=None)

    def test_delete_course_given_too_many_arguments_expect_error(self):
        msg = self.ch.ProcessCommand('delete course Algorithms blah')
        self.assertEqual(msg, 'Invalid number of arguments')

    def test_delete_course_given_too_few_arguments_expect_error(self):
        msg = self.ch.ProcessCommand('delete course')
        self.assertEqual(msg, 'Invalid number of arguments')

    def test_delete_course_with_nonexistent_course_expect_failure(self):
        c = Course.objects.filter(course_name='Databases').first()
        self.assertFalse(c)
        msg = self.ch.ProcessCommand('delete course Databases')
        self.assertEqual(msg, 'A course with that name does not exist')

    def test_delete_course_with_valid_course_expect_success(self):
        c = Course.objects.filter(course_name='Algorithms').first()
        self.assertTrue(c)
        msg = self.ch.ProcessCommand('delete course Algorithms')
        self.assertEqual(msg, 'Delete course: Algorithms')
        c = Course.objects.filter(course_name='Algorithms').first()
        self.assertFalse(c)

class UserAsAdmin(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.admin = Account.objects.create(act_email='super@email.com', role_id=3)
        self.ch.currentUser = self.admin
        Course.objects.create(course_id='535', course_name='Algorithms', instructor=None)


    def test_delete_course_given_too_many_arguments_expect_error(self):
        msg = self.ch.ProcessCommand('delete course Algorithms blah')
        self.assertEqual(msg, 'Invalid number of arguments')

    def test_delete_course_given_too_few_arguments_expect_error(self):
        msg = self.ch.ProcessCommand('delete course')
        self.assertEqual(msg, 'Invalid number of arguments')

    def test_delete_course_with_nonexistent_course_expect_failure(self):
        c = Course.objects.filter(course_name='Databases').first()
        self.assertFalse(c)
        msg = self.ch.ProcessCommand('delete course Databases')
        self.assertEqual(msg, 'A course with that name does not exist')

    def test_delete_course_with_valid_course_expect_success(self):
        c = Course.objects.filter(course_name='Algorithms').first()
        self.assertTrue(c)
        msg = self.ch.ProcessCommand('delete course Algorithms')
        self.assertEqual(msg, 'Delete course: Algorithms')
        c = Course.objects.filter(course_name='Algorithms').first()
        self.assertFalse(c)


class UserAsInstructor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)
        self.ch.currentUser = self.instructor
        Course.objects.create(course_id='535', course_name='Algorithms', instructor=None)

    def test_delete_course_expect_failure(self):
        msg = self.ch.ProcessCommand('delete course Algorithms')
        self.assertEqual(msg, 'Must be logged in as an Administrator or Supervisor')


class UserAsTA(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='test@ta.com', act_fname='test', act_lname='ta', act_phone='1112223333',
                                         act_address='123 test dr', act_officehours='10-11', act_officelocation='123 EMS',
                                         role_id=1)
        self.ch.currentUser = self.ta
        Course.objects.create(course_id='535', course_name='Algorithms', instructor=None)

    def test_delete_course_expect_failure(self):
        msg = self.ch.ProcessCommand('delete course Algorithms')
        self.assertEqual(msg, 'Must be logged in as an Administrator or Supervisor')