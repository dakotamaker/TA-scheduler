from django.test import TestCase
from ..models import Account
from ..models import Course
from ..models import Lab
from ..domain.CommandHandler import CommandHandler
from ..domain.ErrorMessages import ErrorMessages


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
        self.assertEqual(msg, 'Deleted course')
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
        self.assertEqual(msg, 'Deleted course')
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


# delete course <course name>
class CourseAsInvalidUser(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        Course.objects.create(course_name='course1')

    def test_not_logged_in__then_expect_error(self):
        r = self.ch.ProcessCommand('delete course "course1"')
        self.assertEquals('Must be logged in as an Administrator or Supervisor', r)
        self.assertIsNotNone(Course.objects.filter(course_name='course1').first())

    def test_logged_in_not_supervisor_or_administrator__expect_error(self):
        self.ch.currentUser = self.ta
        r = self.ch.ProcessCommand('delete course "course1"')
        self.assertEquals('Must be logged in as an Administrator or Supervisor', r)
        self.assertIsNotNone(Course.objects.filter(course_name='course1').first())


# delete course <course name>
class CourseAsSupervisor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
        self.super = Account.objects.create(act_email='super@email.com', role_id=4)
        self.c1 = Course.objects.create(course_name='course1')
        self.ch.currentUser = self.super

    def test_course_does_not_exist__expect_error(self):
        r = self.ch.ProcessCommand('delete course "dne"')
        self.assertEquals('A course with that name does not exist', r)
        self.assertIsNone(Course.objects.filter(course_name='dne').first())

    def test_happy_path__expect_success(self):
        r = self.ch.ProcessCommand('delete course "course1"')
        self.assertEquals('Deleted course', r)
        self.assertEquals(Course.objects.filter(course_name='course1').count(), 0)

    def test_too_few_args__expect_error(self):
        r = self.ch.ProcessCommand('delete lab "arg1"')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)

    def test_too_many_args__expect_error(self):
        r = self.ch.ProcessCommand('delete lab "arg1" "arg2" "arg3"')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)


# delete course <course name>
class CourseAsAdmin(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
        self.super = Account.objects.create(act_email='super@email.com', role_id=4)
        self.c1 = Course.objects.create(course_name='course1')
        self.ch.currentUser = self.admin

    def test_course_does_not_exist__expect_error(self):
        r = self.ch.ProcessCommand('delete course "dne"')
        self.assertEquals('A course with that name does not exist', r)
        self.assertIsNone(Course.objects.filter(course_name='dne').first())

    def test_happy_path__expect_success(self):
        r = self.ch.ProcessCommand('delete course "course1"')
        self.assertEquals('Deleted course', r)
        self.assertEquals(Course.objects.filter(course_name='course1').count(), 0)

    def test_too_few_args__expect_error(self):
        r = self.ch.ProcessCommand('delete lab "arg1"')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)

    def test_too_many_args__expect_error(self):
        r = self.ch.ProcessCommand('delete lab "arg1" "arg2" "arg3"')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)


# delete lab <course name> <lab name>
class LabAsInvalidUser(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        Course.objects.create(course_name='course1')

    def test_not_logged_in__then_expect_error(self):
        r = self.ch.ProcessCommand('delete lab "course1" "lab1"')
        self.assertEquals('Must be logged in as an Administrator or Supervisor', r)
        self.assertIsNone(Lab.objects.filter(lab_name='lab1').first())

    def test_logged_in_not_supervisor_or_administrator__expect_error(self):
        self.ch.currentUser = self.ta
        r = self.ch.ProcessCommand('delete lab "course1" "lab1"')
        self.assertEquals('Must be logged in as an Administrator or Supervisor', r)
        self.assertIsNone(Lab.objects.filter(lab_name='lab1').first())


# delete lab <course name> <lab name>
class LabAsSupervisor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
        self.super = Account.objects.create(act_email='super@email.com', role_id=4)
        self.c1 = Course.objects.create(course_name='course1')
        self.lab1 = Lab.objects.create(lab_name='lab1', course=self.c1)
        Lab.objects.create(lab_name='lab2', course=self.c1)
        self.ch.currentUser = self.super

    def test_course_does_not_exist__expect_error(self):
        r = self.ch.ProcessCommand('delete lab "dne" "lab2"')
        self.assertEquals('A course with that name does not exist', r)
        self.assertIsNone(Lab.objects.filter(lab_name='dne').first())

    def test_happy_path__expect_success(self):
        r = self.ch.ProcessCommand('delete lab "course1" "lab2"')
        self.assertEquals('Lab deleted', r)
        self.assertEquals(Lab.objects.filter(lab_name='lab2').count(), 0)

    def test_too_few_args__expect_error(self):
        r = self.ch.ProcessCommand('delete lab "arg1"')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)

    def test_too_many_args__expect_error(self):
        r = self.ch.ProcessCommand('delete lab "arg1" "arg2" "arg3"')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)


# delete lab <course name> <lab name>
class LabAsAdministrator(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
        self.super = Account.objects.create(act_email='super@email.com', role_id=4)
        self.c1 = Course.objects.create(course_name='course1')
        self.lab1 = Lab.objects.create(lab_name='lab1', course=self.c1)
        Lab.objects.create(lab_name='lab2', course=self.c1)
        self.ch.currentUser = self.admin

    def test_course_does_not_exist__expect_error(self):
        r = self.ch.ProcessCommand('delete lab "dne" "lab2"')
        self.assertEquals('A course with that name does not exist', r)
        self.assertIsNone(Lab.objects.filter(lab_name='dne').first())

    def test_happy_path__expect_success(self):
        r = self.ch.ProcessCommand('delete lab "course1" "lab2"')
        self.assertEquals('Lab deleted', r)
        self.assertEquals(Lab.objects.filter(lab_name='lab2').count(), 0)

    def test_too_few_args__expect_error(self):
        r = self.ch.ProcessCommand('delete lab "arg1"')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)

    def test_too_many_args__expect_error(self):
        r = self.ch.ProcessCommand('delete lab "arg1" "arg2" "arg3"')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)

