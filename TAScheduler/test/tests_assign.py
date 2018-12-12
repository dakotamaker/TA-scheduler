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
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
        self.c1 = Course.objects.create(course_name='course1')
        Lab.objects.create(lab_name='lab1', course=self.c1)

    def test_logged_in_not_supervisor_or_instructor__expect_error(self):
        self.ch.currentUser = self.ta
        r = self.ch.ProcessCommand('assign lab "course1" "lab1" email@email.com')
        self.assertEquals('Must be logged in as an Instructor or Supervisor', r)
        self.ch.currentUser = self.admin
        r = self.ch.ProcessCommand('assign lab "course1" "lab1" email@email.com')
        self.assertEquals('Must be logged in as an Instructor or Supervisor', r)


# assign lab <course name> <lab name> <ta email>
class LabAsSupervisor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        self.ta2 = Account.objects.create(act_email='ta2@email.com', role_id=1)
        Account.objects.create(act_email='ta_bad@email.com', role_id=1)
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
        self.super = Account.objects.create(act_email='super@email.com', role_id=4)
        self.c1 = Course.objects.create(course_name='course1')
        self.c1.tas.add(self.ta)
        self.c1.tas.add(self.ta2)
        self.lab1 = Lab.objects.create(lab_name='lab1', course=self.c1)
        self.ch.currentUser = self.super

    def test_course_dne__expect_error(self):
        r = self.ch.ProcessCommand('assign lab "dne" "lab1" ta@email.com')
        self.assertEquals('A course with that name does not exist', r)

    def test_lab_dne__expect_error(self):
        r = self.ch.ProcessCommand('assign lab "course1" "dne" ta@email.com')
        self.assertEquals('Lab for that course does not exist', r)

    def test_lab_already_assigned__expect_error(self):
        self.ch.ProcessCommand('assign lab "course1" "lab1" ta2@email.com')
        r = self.ch.ProcessCommand('assign lab "course1" "lab1" ta2@email.com')
        self.assertEquals('This course already has a TA', r)

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
class LabAsInstructor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        self.ta2 = Account.objects.create(act_email='ta2@email.com', role_id=1)
        Account.objects.create(act_email='ta_bad@email.com', role_id=1)
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)
        self.instructor2 = Account.objects.create(act_email='instructor2@email.com', role_id=2)
        self.c1 = Course.objects.create(course_name='course1', instructor=self.instructor)
        self.c1.tas.add(self.ta)
        self.c1.tas.add(self.ta2)
        self.lab1 = Lab.objects.create(lab_name='lab1', course=self.c1)
        self.ch.currentUser = self.instructor

    def test_course_dne__expect_error(self):
        r = self.ch.ProcessCommand('assign lab "dne" "lab1" ta@email.com')
        self.assertEquals('A course with that name does not exist', r)

    def test_instructor_not_assigned_course__expect_error(self):
        self.ch.currentUser = self.instructor2
        r = self.ch.ProcessCommand('assign lab "course1" "lab1" ta@email.com')
        self.assertEqual('Instructors can only assign TAs to their own courses.', r)

    def test_lab_dne__expect_error(self):
        r = self.ch.ProcessCommand('assign lab "course1" "dne" ta@email.com')
        self.assertEquals('Lab for that course does not exist', r)

    def test_lab_already_assigned__expect_error(self):
        self.ch.ProcessCommand('assign lab "course1" "lab1" ta2@email.com')
        r = self.ch.ProcessCommand('assign lab "course1" "lab1" ta2@email.com')
        self.assertEquals('This course already has a TA', r)

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
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
        self.c1 = Course.objects.create(course_name='course1')
        Lab.objects.create(lab_name='lab1', course=self.c1)

    def test_logged_in_not_supervisor_or_instructor__expect_error(self):
        self.ch.currentUser = self.ta
        r = self.ch.ProcessCommand('assign lab "course1" "lab1" email@email.com')
        self.assertEquals('Must be logged in as an Instructor or Supervisor', r)
        self.ch.currentUser = self.admin
        r = self.ch.ProcessCommand('assign lab "course1" "lab1" email@email.com')
        self.assertEquals('Must be logged in as an Instructor or Supervisor', r)


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
class CourseTaAsInstructor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        Account.objects.create(act_email='ta_bad@email.com', role_id=1)
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)
        self.instructor2 = Account.objects.create(act_email='instructor2@email.com', role_id=2)
        self.c1 = Course.objects.create(course_name='course1', instructor=self.instructor)
        self.c1.tas.add(self.ta)
        self.lab1 = Lab.objects.create(lab_name='lab1', course=self.c1)
        self.ch.currentUser = self.instructor

    def test_course_dne__expect_error(self):
        r = self.ch.ProcessCommand('assign course ta "dne" ta@email.com')
        self.assertEquals('A course with that name does not exist', r)

    def test_instructor_not_assigned_course__expect_error(self):
        self.ch.currentUser = self.instructor2
        r = self.ch.ProcessCommand('assign course ta "course1" admin@email.com')
        self.assertEqual('Instructors can only assign TAs to their own courses.', r)

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

# assign course instructor <course name> <instructor email>
class CourseInstructorAsInvalidUser(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)
        self.c1 = Course.objects.create(course_name='course1')

    def test_logged_in_not_supervisor__expect_error(self):
        self.ch.currentUser = self.ta
        r = self.ch.ProcessCommand('assign course instructor "course1" instructor@email.com')
        self.assertEquals('Must be logged in as a Supervisor', r)
        self.ch.currentUser = self.admin
        r = self.ch.ProcessCommand('assign course instructor "course1" instructor@email.com')
        self.assertEquals('Must be logged in as a Supervisor', r)
        self.ch.currentUser = self.instructor
        r = self.ch.ProcessCommand('assign course instructor "course1" instructor@email.com')
        self.assertEquals('Must be logged in as a Supervisor', r)

# assign course instructor <course name> <instructor email>
class CourseInstructorAsSupervisor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)
        self.instructor2 = Account.objects.create(act_email='instructor2@email.com', role_id=2)
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        Account.objects.create(act_email='ta_bad@email.com', role_id=1)
        self.super = Account.objects.create(act_email='super@email.com', role_id=4)
        self.c1 = Course.objects.create(course_name='course1')
        self.ch.currentUser = self.super

    def test_course_dne__expect_error(self):
        r = self.ch.ProcessCommand('assign course instructor "casdf" instructor@email.com')
        self.assertEquals('A course with that name does not exist', r)

    def test_instructor_dne__expect_error(self):
        r = self.ch.ProcessCommand('assign course instructor "course1" instruasdfs@email.com')
        self.assertEquals('This user does not exist', r)

    def test_not_instructor__expect_error(self):
        r = self.ch.ProcessCommand('assign course instructor "course1" ta@email.com')
        self.assertEquals('Assignee must be an instructor', r)

    def test_course_already_assigned__expect_error(self):
        self.ch.ProcessCommand('assign course instructor "course1" instructor2@email.com')
        r = self.ch.ProcessCommand('assign course instructor "course1" instructor@email.com')
        self.assertEquals('This course already has an instructor', r)

    def test_happy_path__expect_success(self):
        r = self.ch.ProcessCommand('assign course instructor "course1" instructor@email.com')
        self.assertEquals('Instructor assigned to course', r)
        self.assertEquals(Course.objects.filter(course_name='course1').first().instructor.act_email, 'instructor@email.com')


    def test_too_few_args__expect_error(self):
        r = self.ch.ProcessCommand('assign course instructor "arg1"')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)

    def test_too_many_args__expect_error(self):
        r = self.ch.ProcessCommand('assign course instructor "arg1" "arg2" "arg3"')
        self.assertEquals(ErrorMessages.INVALID_NUM_OF_ARGUMENTS, r)
