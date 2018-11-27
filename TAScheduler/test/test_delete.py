from django.test import TestCase
from ..models import Account
from ..models import Course
from ..models import Lab
from ..domain.CommandHandler import CommandHandler
from ..domain.ErrorMessages import ErrorMessages


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
