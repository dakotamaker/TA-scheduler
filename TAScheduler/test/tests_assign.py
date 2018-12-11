from django.test import TestCase
from ..models import Account
from ..models import Course
from ..models import Lab
from ..domain.CommandHandler import CommandHandler
from ..domain.ErrorMessages import ErrorMessages


# assign lab <course name> <lab name> <ta email>
class LabAsInvalidUser(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        self.c1 = Course.objects.create(course_name='course1')
        Lab.objects.create(lab_name='lab1', course=self.c1)

    def test_logged_in_not_supervisor_or_administrator__expect_error(self):
        self.ch.currentUser = self.ta
        r = self.ch.ProcessCommand('assign lab "course1" "lab1" email@email.com')
        self.assertEquals('Must be logged in as an Instructor, Administrator or Supervisor', r)


# assign lab <course name> <lab name> <ta email>
class LabAsSupervisor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        Account.objects.create(act_email='ta_bad@email.com', role_id=1)
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
        self.super = Account.objects.create(act_email='super@email.com', role_id=4)
        self.c1 = Course.objects.create(course_name='course1')
        self.c1.tas.add(self.ta)
        self.lab1 = Lab.objects.create(lab_name='lab1', course=self.c1)
        self.ch.currentUser = self.super

    def test_course_dne__expect_error(self):
        r = self.ch.ProcessCommand('assign lab "dne" "lab1" ta@email.com')
        self.assertEquals('A course with that name does not exist', r)

    def test_lab_dne__expect_error(self):
        r = self.ch.ProcessCommand('assign lab "course1" "dne" ta@email.com')
        self.assertEquals('Lab for that course does not exist', r)

    def test_not_ta__expect_error(self):
        r = self.ch.ProcessCommand('assign lab "course1" "lab1" admin@email.com')
        self.assertEquals('Only TAs assigned to the course can be assigned to the lab', r)

    def test_ta_not_assigned_to_course__expect_error(self):
        r = self.ch.ProcessCommand('assign lab "course1" "lab1" ta_bad@email.com')
        self.assertEquals('Only TAs assigned to the course can be assigned to the lab', r)

    def test_happy_path__expect_success(self):
        r = self.ch.ProcessCommand('assign lab "course1" "lab1" ta@email.com')
        self.assertEquals('Assigned TA to lab', r)
        self.assertEquals(Lab.objects.filter(lab_name='lab1').first().ta.act_email, 'ta@email.com')

    def test_too_few_args__expect_error(self):
        r = self.ch.ProcessCommand('assign lab "arg1" arg2')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)

    def test_too_many_args__expect_error(self):
        r = self.ch.ProcessCommand('assign lab "arg1" "arg2" "arg3" arg4')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)


# assign lab <course name> <lab name> <ta email>
class LabAsAdministrator(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        Account.objects.create(act_email='ta_bad@email.com', role_id=1)
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
        self.super = Account.objects.create(act_email='super@email.com', role_id=4)
        self.c1 = Course.objects.create(course_name='course1')
        self.c1.tas.add(self.ta)
        self.lab1 = Lab.objects.create(lab_name='lab1', course=self.c1)
        self.ch.currentUser = self.admin

    def test_course_dne__expect_error(self):
        r = self.ch.ProcessCommand('assign lab "dne" "lab1" ta@email.com')
        self.assertEquals('A course with that name does not exist', r)

    def test_lab_dne__expect_error(self):
        r = self.ch.ProcessCommand('assign lab "course1" "dne" ta@email.com')
        self.assertEquals('Lab for that course does not exist', r)

    def test_not_ta__expect_error(self):
        r = self.ch.ProcessCommand('assign lab "course1" "lab1" admin@email.com')
        self.assertEquals('Only TAs assigned to the course can be assigned to the lab', r)

    def test_ta_not_assigned_to_course__expect_error(self):
        r = self.ch.ProcessCommand('assign lab "course1" "lab1" ta_bad@email.com')
        self.assertEquals('Only TAs assigned to the course can be assigned to the lab', r)

    def test_happy_path__expect_success(self):
        r = self.ch.ProcessCommand('assign lab "course1" "lab1" ta@email.com')
        self.assertEquals('Assigned TA to lab', r)
        self.assertEquals(Lab.objects.filter(lab_name='lab1').first().ta.act_email, 'ta@email.com')

    def test_too_few_args__expect_error(self):
        r = self.ch.ProcessCommand('assign lab "arg1" arg2')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)

    def test_too_many_args__expect_error(self):
        r = self.ch.ProcessCommand('assign lab "arg1" "arg2" "arg3" arg4')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)


# assign course ta <course name> <ta email>
class CourseTaAsInvalidUser(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        self.c1 = Course.objects.create(course_name='course1')
        Lab.objects.create(lab_name='lab1', course=self.c1)

    def test_logged_in_not_supervisor_or_administrator__expect_error(self):
        self.ch.currentUser = self.ta
        r = self.ch.ProcessCommand('assign course ta course1 ta@email.com')
        self.assertEquals('Must be logged in as an Administrator or Supervisor', r)


# assign course ta <course name> <ta email>
class CourseTaAsSupervisor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        Account.objects.create(act_email='ta_bad@email.com', role_id=1)
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
        self.super = Account.objects.create(act_email='super@email.com', role_id=4)
        self.c1 = Course.objects.create(course_name='course1')
        self.c1.tas.add(self.ta)
        self.lab1 = Lab.objects.create(lab_name='lab1', course=self.c1)
        self.ch.currentUser = self.super

    def test_course_dne__expect_error(self):
        r = self.ch.ProcessCommand('assign course ta "dne" ta@email.com')
        self.assertEquals('A course with that name does not exist', r)

    def test_ta_dne__expect_error(self):
        r = self.ch.ProcessCommand('assign course ta "course1" dne@email.com')
        self.assertEquals('Only existing TAs can be assigned to the course', r)

    def test_not_ta__expect_error(self):
        r = self.ch.ProcessCommand('assign course ta "course1" admin@email.com')
        self.assertEquals('Only existing TAs can be assigned to the course', r)

    def test_happy_path__expect_success(self):
        r = self.ch.ProcessCommand('assign course ta "course1" ta@email.com')
        self.assertEquals('TA assigned to course', r)
        self.assertEquals(Course.objects.filter(course_name='course1').first().tas.first().act_email, 'ta@email.com')

    def test_too_few_args__expect_error(self):
        r = self.ch.ProcessCommand('assign course ta "arg1"')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)

    def test_too_many_args__expect_error(self):
        r = self.ch.ProcessCommand('assign course ta "arg1" "arg2" "arg3"')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)


# assign course ta <course name> <ta email>
class CourseTaAsAdministrator(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        Account.objects.create(act_email='ta_bad@email.com', role_id=1)
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
        self.super = Account.objects.create(act_email='super@email.com', role_id=4)
        self.c1 = Course.objects.create(course_name='course1')
        self.c1.tas.add(self.ta)
        self.lab1 = Lab.objects.create(lab_name='lab1', course=self.c1)
        self.ch.currentUser = self.admin

    def test_course_dne__expect_error(self):
        r = self.ch.ProcessCommand('assign course ta "dne" ta@email.com')
        self.assertEquals('A course with that name does not exist', r)

    def test_ta_dne__expect_error(self):
        r = self.ch.ProcessCommand('assign course ta "course1" dne@email.com')
        self.assertEquals('Only existing TAs can be assigned to the course', r)

    def test_not_ta__expect_error(self):
        r = self.ch.ProcessCommand('assign course ta "course1" admin@email.com')
        self.assertEquals('Only existing TAs can be assigned to the course', r)

    def test_happy_path__expect_success(self):
        r = self.ch.ProcessCommand('assign course ta "course1" ta@email.com')
        self.assertEquals('TA assigned to course', r)
        self.assertEquals(Course.objects.filter(course_name='course1').first().tas.first().act_email, 'ta@email.com')

    def test_too_few_args__expect_error(self):
        r = self.ch.ProcessCommand('assign course ta "arg1"')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)

    def test_too_many_args__expect_error(self):
        r = self.ch.ProcessCommand('assign course ta "arg1" "arg2" "arg3"')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)
