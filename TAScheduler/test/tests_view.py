from django.test import TestCase
from ..models import Account
from ..models import Course
from ..models import Lab
from ..domain.CommandHandler import CommandHandler

ALL_TA_INFO_STRING = 'Account email: test@ta.com\nFirst name: test\nLast name: ta\nPhone number: 1112223333\nAddress: 123 test dr\nOffice hours: 10-11\nOffice Location: 123 EMS'
PUBLIC_TA_INFO_STRING = 'Account email: test@ta.com\nFirst name: test\nLast name: ta\nOffice hours: 10-11\nOffice Location: 123 EMS'


class UserAsSupervisor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.admin = Account.objects.create(act_email='super@email.com', role_id=4)
        self.ta = Account.objects.create(act_email='test@ta.com', act_fname='test', act_lname='ta', act_phone='1112223333',
                                         act_address='123 test dr', act_officehours='10-11', act_officelocation='123 EMS',
                                         role_id=1)
        self.ch.currentUser = self.admin

    def test_view_given_too_many_arguments_expect_error(self):
        msg = self.ch.ProcessCommand('view user test@ta.com blah')
        self.assertEqual(msg, 'Invalid number of arguments')

    def test_view_given_too_few_arguments_expect_error(self):
        msg = self.ch.ProcessCommand('view user')
        self.assertEqual(msg, 'Invalid number of arguments')

    def test_view_user_get_all_user_info(self):
        msg = self.ch.ProcessCommand('view user test@ta.com')
        self.assertEqual(msg, ALL_TA_INFO_STRING)

class UserAsAdmin(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.admin = Account.objects.create(act_email='super@email.com', role_id=3)
        self.ta = Account.objects.create(act_email='test@ta.com', act_fname='test', act_lname='ta', act_phone='1112223333',
                                         act_address='123 test dr', act_officehours='10-11', act_officelocation='123 EMS',
                                         role_id=1)
        self.ch.currentUser = self.admin

    def test_view_user_get_all_user_info(self):
        msg = self.ch.ProcessCommand('view user test@ta.com')
        self.assertEqual(msg, ALL_TA_INFO_STRING)


class UserAsInstructor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.admin = Account.objects.create(act_email='super@email.com', role_id=2)
        self.ta = Account.objects.create(act_email='test@ta.com', act_fname='test', act_lname='ta', act_phone='1112223333',
                                         act_address='123 test dr', act_officehours='10-11', act_officelocation='123 EMS',
                                         role_id=1)
        self.ch.currentUser = self.admin

    def test_view_user_get_all_public_user_info(self):
        msg = self.ch.ProcessCommand('view user test@ta.com')
        self.assertEqual(msg, PUBLIC_TA_INFO_STRING)


class UserAsTA(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.admin = Account.objects.create(act_email='super@email.com', role_id=1)
        self.ta = Account.objects.create(act_email='test@ta.com', act_fname='test', act_lname='ta', act_phone='1112223333',
                                         act_address='123 test dr', act_officehours='10-11', act_officelocation='123 EMS',
                                         role_id=1)
        self.ch.currentUser = self.admin

    def test_view_user_get_all_public_user_info(self):
        msg = self.ch.ProcessCommand('view user test@ta.com')
        self.assertEqual(msg, PUBLIC_TA_INFO_STRING)
