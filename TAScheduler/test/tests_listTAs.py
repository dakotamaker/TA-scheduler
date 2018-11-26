from django.test import TestCase
from ..models import Account
from ..models import Course
from ..models import Lab
from ..domain.CommandHandler import CommandHandler
from ..domain.ErrorMessages import ErrorMessages

class ListTAsTestCase(TestCase):
    def setUp(self):
        self.super = Account.objects.create(act_email='super@email.com', act_fname='Super', act_lname='Visor',
                               act_password='4444', act_address='123 main st.', act_phone='444-444-4444', role_id=4,
                               act_officehours="11-12", act_officelocation="EMS 124")
        self.admin = Account.objects.create(act_email='admin@email.com', act_fname='Admin', act_lname='Istrator',
                               act_password='3333', act_address='10 First st.', act_phone='333-333-3333', role_id=3,
                               act_officehours="9-10", act_officelocation="EMS 123")
        self.instructor = Account.objects.create(act_email='instructor@email.com', act_fname='Instr', act_lname='Uctor',
                               act_password='2222', act_address='17 North st.', act_phone='222-222-2222', role_id=2,
                               act_officehours="10-11", act_officelocation="EMS 122")
        self.ta1 = Account.objects.create(act_email='ta1@email.com', act_fname='TA1', act_lname='Student',
                               act_password='1111', act_address='24 Second St', act_phone='111-111-1111', role_id=1,
                               act_officehours="1-2", act_officelocation="EMS 121")
        self.ta2 = Account.objects.create(act_email='ta2@email.com', act_fname='TA2', act_lname='Student',
                               act_password='1111', act_address='24 Second St', act_phone='111-111-1111', role_id=1,
                               act_officehours="1-2", act_officelocation="EMS 121")
        self.ta3 = Account.objects.create(act_email='ta3@email.com', act_fname='TA3', act_lname='Student',
                               act_password='1111', act_address='24 Second St', act_phone='111-111-1111', role_id=1,
                               act_officehours="1-2", act_officelocation="EMS 121")
        self.ta4 = Account.objects.create(act_email='ta4@email.com', act_fname='TA4', act_lname='Student',
                               act_password='1111', act_address='24 Second St', act_phone='111-111-1111', role_id=1,
                               act_officehours="1-2", act_officelocation="EMS 121")

        self.course1 = Course.objects.create(course_id='535', course_name='Algorithms', instructor=self.instructor)
        self.course1.tas.set([self.ta1, self.ta3])
        self.lab1 = Lab.objects.create(lab_id='1', lab_name='AlgoLab', course=self.course1, ta=self.ta1)

        self.course2 = Course.objects.create(course_id='557', course_name='Databases', instructor=self.instructor)
        self.course2.tas.set([self.ta2, self.ta3])
        self.lab2 = Lab.objects.create(lab_id='2', lab_name='DataLab', course=self.course2, ta=self.ta2)




    def test_without_valid_login__then_list_fails(self):
        ch = CommandHandler()
        msg = ch.ProcessCommand("list tas")
        self.assertEqual(msg, 'Must be logged in to access TA list.')

    def test_with_loggedInUser__then_list_succeeds(self):
        ch = CommandHandler()
        ch.ProcessCommand("login ta1@email.com 1111")
        msg = ch.ProcessCommand("list tas")
        self.assertEqual(msg, 'List TAs: \nTA1 Student: Algorithms\tAlgoLab\t\nTA2 Student: Databases\tDataLab\t\nTA3 Student: Algorithms\tDatabases\t\nTA4 Student: ')

