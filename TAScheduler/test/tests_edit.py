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


# edit user email attr
    def test_without_valid_login_edit_self__then_edits_fail(self):
        ch = CommandHandler()
        msg = ch.ProcessCommand("edit act_password:'1234'")
        self.assertEqual(msg, ErrorMessages.NOT_LOGGED_IN)

    def test_without_valid_login_edit_others__then_edits_fail(self):
        ch = CommandHandler()
        msg = ch.ProcessCommand("edit user ta@email.com act_password:'1234'")
        self.assertEqual(msg, ErrorMessages.NOT_LOGGED_IN)

    def test_with_supervisor_editing_self__then_edits_occur(self):
        ch = CommandHandler()
        ch.ProcessCommand("login super@email.com 4444")
        a = Account.objects.get(act_email="super@email.com")
        self.assertEqual(a.act_phone, '444-444-4444')
        msg = ch.ProcessCommand("edit act_phone:'123-456-7890'")
        self.assertEqual(msg, "Edit successful")
        a = Account.objects.get(act_email="super@email.com")
        self.assertEqual(a.act_phone, '123-456-7890')

    def test_with_supervisor_editing_others__then_edits_occur(self):
        ch = CommandHandler()
        ch.ProcessCommand("login super@email.com 4444")
        a = Account.objects.get(act_email="ta@email.com")
        self.assertEqual(a.act_phone, '111-111-1111')
        msg = ch.ProcessCommand("edit user ta@email.com act_phone:'123-456-7890'")
        self.assertEqual(msg, "Edit successful")
        a = Account.objects.get(act_email="ta@email.com")
        self.assertEqual(a.act_phone, '123-456-7890')

    def test_with_supervisor_editing_other_with_invalid_email__then_edits_fail(self):
        ch = CommandHandler()
        ch.ProcessCommand("login super@email.com 4444")
        msg = ch.ProcessCommand("edit user blah@email.com act_phone:'123-456-7890'")
        self.assertEqual(msg, "Given email does not belong to an existing user")

    def test_with_administrator_editing_self__then_edits_occur(self):
        ch = CommandHandler()
        ch.ProcessCommand("login admin@email.com 3333")
        a = Account.objects.get(act_email="admin@email.com")
        self.assertEqual(a.act_phone, '333-333-3333')
        msg = ch.ProcessCommand("edit act_phone:'123-456-7890'")
        self.assertEqual(msg, "Edit successful")
        a = Account.objects.get(act_email="admin@email.com")
        self.assertEqual(a.act_phone, '123-456-7890')

    def test_with_administrator_editing_others__then_edits_occur(self):
        ch = CommandHandler()
        ch.ProcessCommand("login admin@email.com 3333")
        a = Account.objects.get(act_email="ta@email.com")
        self.assertEqual(a.act_phone, '111-111-1111')
        msg = ch.ProcessCommand("edit user ta@email.com act_phone:'123-456-7890'")
        self.assertEqual(msg, "Edit successful")
        a = Account.objects.get(act_email="ta@email.com")
        self.assertEqual(a.act_phone, '123-456-7890')

    def test_with_administrator_editing_other_with_invalid_email__then_edits_fail(self):
        ch = CommandHandler()
        ch.ProcessCommand("login admin@email.com 3333")
        msg = ch.ProcessCommand("edit user blah@email.com act_phone:'123-456-7890'")
        self.assertEqual(msg, "Given email does not belong to an existing user")

    def test_with_instructor_editing_self__then_edits_occur(self):
        ch = CommandHandler()
        ch.ProcessCommand("login instructor@email.com 2222")
        a = Account.objects.get(act_email="instructor@email.com")
        self.assertEqual(a.act_phone, '222-222-2222')
        msg = ch.ProcessCommand("edit act_phone:'123-456-7890'")
        self.assertEqual(msg, "Edit successful")
        a = Account.objects.get(act_email="instructor@email.com")
        self.assertEqual(a.act_phone, '123-456-7890')

    def test_with_instructor_editing_others__then_edits_fail(self):
        ch = CommandHandler()
        ch.ProcessCommand("login instructor@email.com 2222")
        a = Account.objects.get(act_email="ta@email.com")
        self.assertEqual(a.act_phone, '111-111-1111')
        msg = ch.ProcessCommand("edit user ta@email.com act_phone:'123-456-7890'")
        self.assertEqual(msg, 'Only supervisors or admins can edit another user')
        a = Account.objects.get(act_email="ta@email.com")
        self.assertEqual(a.act_phone, '111-111-1111')


    def test_with_ta_editing_self__then_edits_occur(self):
        ch = CommandHandler()
        ch.ProcessCommand("login ta@email.com 1111")
        a = Account.objects.get(act_email="ta@email.com")
        self.assertEqual(a.act_phone, '111-111-1111')
        msg = ch.ProcessCommand("edit act_phone:'123-456-7890'")
        self.assertEqual(msg, "Edit successful")
        a = Account.objects.get(act_email="ta@email.com")
        self.assertEqual(a.act_phone, '123-456-7890')

    def test_with_ta_editing_others__then_edits_fail(self):
        ch = CommandHandler()
        ch.ProcessCommand("login ta@email.com 1111")
        a = Account.objects.get(act_email="instructor@email.com")
        self.assertEqual(a.act_phone, '222-222-2222')
        msg = ch.ProcessCommand("edit user instructor@email.com act_phone:'123-456-7890'")
        self.assertEqual(msg, 'Only supervisors or admins can edit another user')
        a = Account.objects.get(act_email="instructor@email.com")
        self.assertEqual(a.act_phone, '222-222-2222')

    def test_given_too_few_arguments__then_edits_fail(self):
        ch = CommandHandler()
        ch.ProcessCommand("login super@email.com 4444")
        msg = ch.ProcessCommand(edit)
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)

    def test_given_too_many_arguments__then_edits_fail(self):
        ch = CommandHandler()
        ch.ProcessCommand("login super@email.com 4444")
        msg = ch.ProcessCommand("edit act_phone:'555-555-5555' hi")
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        msg = ch.ProcessCommand("edit user ta@email.com act_phone:'555-555-5555' hi")
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)

    def test_given_no_semicolon_on_edit_self__then_edits_fail(self):
        ch = CommandHandler()
        ch.ProcessCommand("login super@email.com 4444")
        msg = ch.ProcessCommand("edit act_phone'555-555-5555'")
        self.assertEqual(msg, "To edit an account you need a semicolon")

    def test_given_no_semicolon_on_edit_self__then_edits_fail(self):
        ch = CommandHandler()
        ch.ProcessCommand("login super@email.com 4444")
        msg = ch.ProcessCommand("edit user admin@email.com act_phone'555-555-5555'")
        self.assertEqual(msg, "To edit an account you need a semicolon")