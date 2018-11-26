from django.test import TestCase
from ..models import Account
from ..models import Course
from ..domain.CommandHandler import CommandHandler
from ..domain.ErrorMessages import ErrorMessages

class EditTestCase(TestCase):
    def setUp(self):
        Account.objects.create(act_email='super@email.com', act_fname='Super', act_lname='Visor',
                               act_password='4444', act_address='123 main st.', act_phone='444-444-4444', role_id=4,
                               act_officehours="11-12", act_officelocation="EMS 124")
        Account.objects.create(act_email='admin@email.com', act_fname='Admin', act_lname='Istrator',
                               act_password='3333', act_address='10 First st.', act_phone='333-333-3333', role_id=3,
                               act_officehours="9-10", act_officelocation="EMS 123")
        self.inst1 = Account.objects.create(act_email='instructor@email.com', act_fname='Instr', act_lname='Uctor',
                               act_password='2222', act_address='17 North st.', act_phone='222-222-2222', role_id=2,
                               act_officehours="10-11", act_officelocation="EMS 122")
        self.inst2 = Account.objects.create(act_email='instructor2@email.com', act_fname='Instr2', act_lname='Uctor2',
                               act_password='22222', act_address='172 North st.', act_phone='222-222-2223', role_id=2,
                               act_officehours="10-12", act_officelocation="EMS 120")
        Account.objects.create(act_email='ta@email.com', act_fname='TA', act_lname='Student',
                               act_password='1111', act_address='24 Second St', act_phone='111-111-1111', role_id=1,
                               act_officehours="1-2", act_officelocation="EMS 121")

        Course.objects.create(course_id='535', course_name='Algorithms', instructor=None)
        Course.objects.create(course_id='537', course_name='OS', instructor=self.inst2)


    def test_without_login__assignment_fails(self):
        ch = CommandHandler()
        msg = ch.ProcessCommand("assign course instructor Algorithms instructor@email.com")
        self.assertEqual(msg, 'Must be logged in as an Administrator or Supervisor')

    def test_supervisor_assigns_valid_instructor_and_valid_class__then_assign_succeeds(self):
        ch = CommandHandler()
        ch.ProcessCommand("login super@email.com 4444")
        c = Course.objects.get(course_name='Algorithms')
        self.assertEquals(c.instructor, None)
        msg = ch.ProcessCommand("assign course instructor Algorithms instructor@email.com")
        self.assertEqual(msg, 'Instructor assigned to course')
        c = Course.objects.get(course_name='Algorithms')
        self.assertEquals(c.instructor, self.inst1)

    def test_supervisor_assigns_nonexistent_user_and_valid_class__then_assign_fails(self):
        ch = CommandHandler()
        ch.ProcessCommand("login super@email.com 4444")
        c = Course.objects.get(course_name='Algorithms')
        self.assertEquals(c.instructor, None)
        msg = ch.ProcessCommand("assign course instructor Algorithms instruc@email.com")
        self.assertEqual(msg, 'This user does not exist')
        c = Course.objects.get(course_name='Algorithms')
        self.assertEquals(c.instructor, None)

    def test_supervisor_assigns_non_instructor_and_valid_class__then_assign_fails(self):
        ch = CommandHandler()
        ch.ProcessCommand("login super@email.com 4444")
        c = Course.objects.get(course_name='Algorithms')
        self.assertEquals(c.instructor, None)
        msg = ch.ProcessCommand("assign course instructor Algorithms admin@email.com")
        self.assertEqual(msg, 'Assignee must be an instructor')
        c = Course.objects.get(course_name='Algorithms')
        self.assertEquals(c.instructor, None)

    def test_supervisor_assigns_valid_instructor_and_invalid_class__then_assign_fails(self):
        ch = CommandHandler()
        ch.ProcessCommand("login super@email.com 4444")
        msg = ch.ProcessCommand("assign course instructor Algorit instructor@email.com")
        self.assertEqual(msg, 'This course does not exist')

    def test_administrator_assigns_valid_instructor_and_valid_class__then_assign_succeeds(self):
        ch = CommandHandler()
        ch.ProcessCommand("login admin@email.com 3333")
        c = Course.objects.get(course_name='Algorithms')
        self.assertEquals(c.instructor, None)
        msg = ch.ProcessCommand("assign course instructor Algorithms instructor@email.com")
        self.assertEqual(msg, 'Instructor assigned to course')
        c = Course.objects.get(course_name='Algorithms')
        self.assertEquals(c.instructor, self.inst1)

    def test_administrator_assigns_nonexistent_user_and_valid_class__then_assign_fails(self):
        ch = CommandHandler()
        ch.ProcessCommand("login admin@email.com 3333")
        c = Course.objects.get(course_name='Algorithms')
        self.assertEquals(c.instructor, None)
        msg = ch.ProcessCommand("assign course instructor Algorithms instruc@email.com")
        self.assertEqual(msg, 'This user does not exist')
        c = Course.objects.get(course_name='Algorithms')
        self.assertEquals(c.instructor, None)

    def test_administrator_assigns_non_instructor_and_valid_class__then_assign_fails(self):
        ch = CommandHandler()
        ch.ProcessCommand("login admin@email.com 3333")
        c = Course.objects.get(course_name='Algorithms')
        self.assertEquals(c.instructor, None)
        msg = ch.ProcessCommand("assign course instructor Algorithms super@email.com")
        self.assertEqual(msg, 'Assignee must be an instructor')
        c = Course.objects.get(course_name='Algorithms')
        self.assertEquals(c.instructor, None)

    def test_administrator_assigns_valid_instructor_and_invalid_class__then_assign_fails(self):
        ch = CommandHandler()
        ch.ProcessCommand("login super@email.com 4444")
        msg = ch.ProcessCommand("assign course instructor Algorit instructor@email.com")
        self.assertEqual(msg, 'This course does not exist')

    def test_instructor_assigns__then_assign_fails(self):
        ch = CommandHandler()
        ch.ProcessCommand("login instructor2@email.com 22222")
        msg = ch.ProcessCommand("assign course instructor Algorithms instructor@email.com")
        self.assertEqual(msg, 'Must be logged in as an Administrator or Supervisor')

    def test_ta_assigns__then_assign_fails(self):
        ch = CommandHandler()
        ch.ProcessCommand("login ta@email.com 1111")
        msg = ch.ProcessCommand("assign course instructor Algorithms instructor@email.com")
        self.assertEqual(msg, 'Must be logged in as an Administrator or Supervisor')

    def test_course_already_has_instructor__then_assign_fails(self):
        ch = CommandHandler()
        ch.ProcessCommand("login super@email.com 4444")
        c = Course.objects.get(course_name='OS')
        self.assertEquals(c.instructor, self.inst2)
        msg = ch.ProcessCommand("assign course instructor OS instructor@email.com")
        self.assertEqual(msg, 'This course already has an instructor')
        c = Course.objects.get(course_name='OS')
        self.assertEquals(c.instructor, self.inst2)

    def test_given_too_few_arguments__then_assign_fails(self):
        ch = CommandHandler()
        ch.ProcessCommand("login admin@email.com 3333")
        c = Course.objects.get(course_name='Algorithms')
        self.assertEquals(c.instructor, None)
        msg = ch.ProcessCommand("assign course instructor Algorithms")
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        c = Course.objects.get(course_name='Algorithms')
        self.assertEquals(c.instructor, None)

    def test_given_too_many_arguments__then_assign_fails(self):
        ch = CommandHandler()
        ch.ProcessCommand("login admin@email.com 3333")
        c = Course.objects.get(course_name='Algorithms')
        self.assertEquals(c.instructor, None)
        msg = ch.ProcessCommand("assign course instructor Algorithms instructor@email.com ta@email.com")
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        c = Course.objects.get(course_name='Algorithms')
        self.assertEquals(c.instructor, None)


