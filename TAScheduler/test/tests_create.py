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


class UserAsAdministrator(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
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


class UserAsTaOrInstructor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)

    def test_creating_a_user_given_all_valid_arguments_as_instrcutor_then_error_is_thrown(self):
        self.ch.currentUser = self.instructor
        msg = self.ch.ProcessCommand('create user new@test.com new user 0 1112223333 \"test st\" \"10-11\" \"EMS 123\"')
        self.assertEqual(msg, 'Must be logged in as an Administrator or Supervisor')

    def test_creating_a_user_given_all_valid_arguments_as_ta_then_error_is_thrown(self):
        self.ch.currentUser = self.ta
        msg = self.ch.ProcessCommand('create user new@test.com new user 0 1112223333 \"test st\" \"10-11\" \"EMS 123\"')
        self.assertEqual(msg, 'Must be logged in as an Administrator or Supervisor')


class CourseAsSupervisor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.super = Account.objects.create(act_email='super@email.com', role_id=4)
        self.ch.currentUser = self.super

    def test_with_supervisor_adding_new_course__then_course_created(self):
        c = Course.objects.filter(course_name='Algorithms')
        self.assertEquals(c.count(), 0)
        msg = self.ch.ProcessCommand("create course 'Algorithms'")
        self.assertEqual(msg, 'Course added')
        c = Course.objects.filter(course_name='Algorithms')
        self.assertEquals(c.count(), 1)

    def test_with_supervisor_adding_existing_course__then_create_fails(self):
        self.ch.ProcessCommand("create course 'Algorithms'")
        msg = self.ch.ProcessCommand("create course 'Algorithms'")
        self.assertEqual(msg, 'Course already exists')
        c = Course.objects.filter(course_name='Algorithms')
        self.assertEquals(c.count(), 1)


class CourseAsAdmin(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=4)
        self.ch.currentUser = self.admin

    def test_with_admin_adding_new_course__then_course_created(self):
        c = Course.objects.filter(course_name='Algorithms')
        self.assertEquals(c.count(), 0)
        msg = self.ch.ProcessCommand("create course 'Algorithms'")
        self.assertEqual(msg, 'Course added')
        c = Course.objects.filter(course_name='Algorithms')
        self.assertEquals(c.count(), 1)

    def test_with_admin_adding_existing_course__then_create_fails(self):
        self.ch.ProcessCommand("create course 'Algorithms'")
        msg = self.ch.ProcessCommand("create course 'Algorithms'")
        self.assertEqual(msg, 'Course already exists')
        c = Course.objects.filter(course_name='Algorithms')
        self.assertEquals(c.count(), 1)


class CourseAsInvalidUser(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)

    def test_with_instructor__then_create_fails(self):
        self.ch.currentUser = self.instructor
        msg = self.ch.ProcessCommand("create course 'Algorithms'")
        self.assertEqual(msg, 'Must be logged in as an Administrator or Supervisor')
        c = Course.objects.filter(course_name='Algorithms')
        self.assertEquals(c.count(), 0)

    def test_with_ta__then_create_fails(self):
        self.ch.currentUser = self.ta
        msg = self.ch.ProcessCommand("create course 'Algorithms'")
        self.assertEqual(msg, 'Must be logged in as an Administrator or Supervisor')
        c = Course.objects.filter(course_name='Algorithms')
        self.assertEquals(c.count(), 0)


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
