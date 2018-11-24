from django.test import TestCase
from ..models import Account
from ..models import Course

class CreateCoursesTestCase(TestCase):
    def setUp(self):
        Account.objects.create(act_email='super@email.com', act_fname='Super', act_lname='Visor',
                               act_password='4444', act_address='123 main st.', act_phone='444-444-4444', role_id=4,
                               act_officehours="11-12", act_officelocation="EMS 124")
        Account.objects.create(act_email='admin@email.com', act_fname='Admin', act_lname='Istrator',
                               act_password='3333', act_address='10 First st.', act_phone='333-333-3333', role_id=3,
                               act_officehours="9-10", act_officelocation="EMS 123")
        Account.objects.create(act_email='instructor@email.com', act_fname='Instr', act_lname='Uctor',
                               act_password='2222', act_address='17 North st.', act_phone='222-222-2222', role_id=2,
                               act_officehours="10-11", act_officelocation="EMS 122")
        Account.objects.create(act_email='ta@email.com', act_fname='TA', act_lname='Student',
                               act_password='1111', act_address='24 Second St', act_phone='111-111-1111', role_id=1,
                               act_officehours="1-2", act_officelocation="EMS 121")

        Course.objects.create(course_id='535', course_name='Algorithms', instructor=instructor@email.com, tas=ta@email.com)

    def test_without_valid_login__then_create_fails(self):
        pass

    def test_with_supervisor_adding_new_course__then_course_created(self):
        pass

    def test_with_supervisor_adding_existing_course__then_create_fails(self):
        pass

    def test_with_administrator_adding_new_course__then_course_created(self):
        pass

    def test_with_administrator_adding_existing_course__then_create_fails(self):
        pass

    def test_with_instructor__then_create_fails(self):
        pass

    def test_with_ta__then_create_fails(self):
        pass

    def test_given_too_few_arguments__then_create_fails(self):
        pass

    def test_given_too_many_arguments__then_create_fails(self):
        pass
