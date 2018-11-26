from django.test import TestCase
from ..models import Account
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
        Account.objects.create(act_email='instructor@email.com', act_fname='Instr', act_lname='Uctor',
                               act_password='2222', act_address='17 North st.', act_phone='222-222-2222', role_id=2,
                               act_officehours="10-11", act_officelocation="EMS 122")
        Account.objects.create(act_email='ta@email.com', act_fname='TA', act_lname='Student',
                               act_password='1111', act_address='24 Second St', act_phone='111-111-1111', role_id=1,
                               act_officehours="1-2", act_officelocation="EMS 121")

    def test_without_login__then_delete_fails(self):
        ch = CommandHandler()
        a = Account.objects.filter(act_email="ta@email.com")
        self.assertEquals(a.count(), 1)
        msg = ch.ProcessCommand("delete user ta@email.com")
        self.assertEqual(msg, 'Must be logged in as an Administrator or Supervisor')
        a = Account.objects.filter(act_email="ta@email.com")
        self.assertEquals(a.count(), 1)

    def test_supervisor_deletes_existing_account__then_delete_succeeds(self):
        ch = CommandHandler()
        ch.ProcessCommand("login super@email.com 4444")
        a = Account.objects.filter(act_email="ta@email.com")
        self.assertEquals(a.count(), 1)
        msg = ch.ProcessCommand("delete user ta@email.com")
        self.assertEqual(msg, "Deleted user ta@email.com")
        a = Account.objects.filter(act_email="ta@email.com")
        self.assertEquals(a.count(), 0)

    def test_supervisor_deletes_nonexistent_account__then_delete_fails(self):
        ch = CommandHandler()
        ch.ProcessCommand("login super@email.com 4444")
        a = Account.objects.filter(act_email="asdf")
        self.assertEquals(a.count(), 0)
        msg = ch.ProcessCommand("delete user asdf")
        self.assertEqual(msg, "Given email does not belong to an existing user")
        a = Account.objects.filter(act_email="asdf")
        self.assertEquals(a.count(), 0)

    def test_administrator_deletes_existing_account__then_delete_succeeds(self):
        ch = CommandHandler()
        ch.ProcessCommand("login admin@email.com 3333")
        a = Account.objects.filter(act_email="ta@email.com")
        self.assertEquals(a.count(), 1)
        msg = ch.ProcessCommand("delete user ta@email.com")
        self.assertEqual(msg, "Deleted user ta@email.com")
        a = Account.objects.filter(act_email="ta@email.com")
        self.assertEquals(a.count(), 0)

    def test_administrator_deletes_nonexistent_account__then_delete_fails(self):
        ch = CommandHandler()
        ch.ProcessCommand("login admin@email.com 3333")
        a = Account.objects.filter(act_email="asdf")
        self.assertEquals(a.count(), 0)
        msg = ch.ProcessCommand("delete user asdf")
        self.assertEqual(msg, "Given email does not belong to an existing user")
        a = Account.objects.filter(act_email="asdf")
        self.assertEquals(a.count(), 0)

    def test_instructor_deletes_account__then_delete_fails(self):
        ch = CommandHandler()
        ch.ProcessCommand("login instructor@email.com 2222")
        a = Account.objects.filter(act_email="ta@email.com")
        self.assertEquals(a.count(), 1)
        msg = ch.ProcessCommand("delete user ta@email.com")
        self.assertEqual(msg, 'Must be logged in as an Administrator or Supervisor')
        a = Account.objects.filter(act_email="ta@email.com")
        self.assertEquals(a.count(), 1)

    def test_ta_deletes_account__then_delete_fails(self):
        ch = CommandHandler()
        ch.ProcessCommand("login ta@email.com 1111")
        a = Account.objects.filter(act_email="instructor@email.com")
        self.assertEquals(a.count(), 1)
        msg = ch.ProcessCommand("delete user instructor@email.com")
        self.assertEqual(msg, 'Must be logged in as an Administrator or Supervisor')
        a = Account.objects.filter(act_email="instructor@email.com")
        self.assertEquals(a.count(), 1)

    def test_given_too_few_arguments__then_delete_fails(self):
        ch = CommandHandler()
        ch.ProcessCommand("login super@email.com 4444")
        msg = ch.ProcessCommand("delete user")
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)

    def test_given_too_many_arguments__then_delete_fails(self):
        ch = CommandHandler()
        ch.ProcessCommand("login super@email.com 4444")
        msg = ch.ProcessCommand("delete user ta@email.com asdf")
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)

    def test_user_deletes_account_twice__then_second_delete_fails(self):
        ch = CommandHandler()
        ch.ProcessCommand("login super@email.com 4444")
        a = Account.objects.filter(act_email="ta@email.com")
        self.assertEquals(a.count(), 1)
        ch.ProcessCommand("delete user ta@email.com")
        a = Account.objects.filter(act_email="ta@email.com")
        self.assertEquals(a.count(), 0)
        msg = ch.ProcessCommand("delete user ta@email.com")
        self.assertEqual(msg, "Given email does not belong to an existing user")
        a = Account.objects.filter(act_email="ta@email.com")
        self.assertEquals(a.count(), 0)