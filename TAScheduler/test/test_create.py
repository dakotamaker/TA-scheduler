from django.test import TestCase
from ..models import Account
from ..models import Course
from ..models import Lab
from ..domain.CommandHandler import CommandHandler
from ..domain.ErrorMessages import ErrorMessages


class UserAsAdministrator(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.admin = Account.objects.create(act_email='super@email.com', role_id=3)
        self.ta = Account.objects.create(act_email='ta1@ta.com', role_id=1)
        self.ch.currentUser = self.admin

    def test_creating_a_user_given_all_valid_arguments_then_user_is_created(self):
        self.ch.ProcessCommand('create user new@test.com new user 0 1112223333 \"test st\" \"10-11\" \"EMS 123\"')
        self.assertIsNotNone(Account.objects.filter(act_email='new@test.com').first())

    def test_creating_a_user_given_user_already_exits_then_no_new_user_is_created(self):
        msg = self.ch.ProcessCommand('create user ta1@ta.com new user 0 1112223333 \"test st\" \"10-11\" \"EMS 123\"')
        self.assertEqual(msg, 'User already exists')

    def test_creating_a_user_given_too_few_arguments_then_error_is_displayed(self):
        msg = self.ch.ProcessCommand('create user new@test.com new test-user ta \"test st\"')
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)

    def test_creating_a_user_given_too_many_arguments_then_error_is_displayed(self):
        msg = self.ch.ProcessCommand('create user new@test.com new test-user ta 1112223333 \"test st\" too-many-arguments')
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)

# create lab <course name> <lab name>
class LabAsInvalidUser(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        Course.objects.create(course_name='course1')

    def test_not_logged_in__then_expect_error(self):
        r = self.ch.ProcessCommand('create lab "course1" "lab1"')
        self.assertEquals('Must be logged in as an Administrator or Supervisor', r)
        self.assertIsNone(Lab.objects.filter(lab_name='lab1').first())

    def test_logged_in_not_supervisor_or_administrator__expect_error(self):
        self.ch.currentUser = self.ta
        r = self.ch.ProcessCommand('create lab "course1" "lab1"')
        self.assertEquals('Must be logged in as an Administrator or Supervisor', r)
        self.assertIsNone(Lab.objects.filter(lab_name='lab1').first())


# create lab <course name> <lab name>
class LabAsSupervisor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
        self.super = Account.objects.create(act_email='super@email.com', role_id=4)
        self.c1 = Course.objects.create(course_name='course1')
        self.lab1 = Lab.objects.create(lab_name='lab1', course=self.c1)
        self.ch.currentUser = self.super

    def test_course_dne__expect_error(self):
        r = self.ch.ProcessCommand('create lab "dne" "lab2"')
        self.assertEquals('A course with that name does not exist', r)
        self.assertIsNone(Lab.objects.filter(lab_name='lab2').first())

    def test_lab_exists__expect_error(self):
        r = self.ch.ProcessCommand('create lab "course1" "lab1"')
        self.assertEquals('A lab with that name already exists for this course', r)
        self.assertEquals(Lab.objects.filter(lab_name='lab1').count(), 1)

    def test_happy_path__expect_success(self):
        r = self.ch.ProcessCommand('create lab "course1" "lab2"')
        self.assertEquals('Lab created', r)
        self.assertEquals(Lab.objects.filter(lab_name='lab2').count(), 1)

    def test_too_few_args__expect_error(self):
        r = self.ch.ProcessCommand('create lab "arg1"')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)

    def test_too_many_args__expect_error(self):
        r = self.ch.ProcessCommand('create lab "arg1" "arg2" "arg3"')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)


# create lab <course name> <lab name>
class LabAsAdministrator(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
        self.super = Account.objects.create(act_email='super@email.com', role_id=4)
        self.c1 = Course.objects.create(course_name='course1')
        self.lab1 = Lab.objects.create(lab_name='lab1', course=self.c1)
        self.ch.currentUser = self.admin

    def test_course_dne__expect_error(self):
        r = self.ch.ProcessCommand('create lab "dne" "lab2"')
        self.assertEquals('A course with that name does not exist', r)
        self.assertIsNone(Lab.objects.filter(lab_name='lab2').first())

    def test_lab_exists__expect_error(self):
        r = self.ch.ProcessCommand('create lab "course1" "lab1"')
        self.assertEquals('A lab with that name already exists for this course', r)
        self.assertEquals(Lab.objects.filter(lab_name='lab1').count(), 1)

    def test_happy_path__expect_success(self):
        r = self.ch.ProcessCommand('create lab "course1" "lab2"')
        self.assertEquals('Lab created', r)
        self.assertEquals(Lab.objects.filter(lab_name='lab2').count(), 1)

    def test_too_few_args__expect_error(self):
        r = self.ch.ProcessCommand('create lab "arg1"')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)

    def test_too_many_args__expect_error(self):
        r = self.ch.ProcessCommand('create lab "arg1" "arg2" "arg3"')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)
