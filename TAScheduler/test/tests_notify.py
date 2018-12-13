from django.test import TestCase
from ..models import Account
from ..models import Course
from ..domain.CommandHandler import CommandHandler


class NotifyAsSupervisor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.super = Account.objects.create(act_email='super@email.com', role_id=4)
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        self.ch.currentUser = self.super

    def test_notify_user_given_valid_arguments_then_notification_is_sent(self):
        msg = self.ch.ProcessCommand('notify ta@email.com "test subject" "test body"')
        self.assertEqual(msg, 'Notification email sent to ta@email.com!')

    def test_notify_user_that_does_not_exist_then_error_occurs(self):
        msg = self.ch.ProcessCommand('notify invalid@email.com "test subject" "test body"')
        self.assertEqual(msg, 'This user does not exist')

    def test_notify_user_given_too_many_arguments_then_error_occurs(self):
        msg = self.ch.ProcessCommand('notify ta@email.com "test subject" test body')
        self.assertEqual(msg, 'Invalid number of arguments')

    def test_notify_user_given_too_few_arguments_then_error_occurs(self):
        msg = self.ch.ProcessCommand('notify ta@email.com "test subject"')
        self.assertEqual(msg, 'Invalid number of arguments')
        

class NotifyAsAdmin(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.super = Account.objects.create(act_email='super@email.com', role_id=4)
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        self.ch.currentUser = self.admin

    def test_notify_user_given_valid_arguments_then_notification_is_sent(self):
        msg = self.ch.ProcessCommand('notify ta@email.com "test subject" "test body"')
        self.assertEqual(msg, 'Notification email sent to ta@email.com!')

    def test_notify_user_that_does_not_exist_then_error_occurs(self):
        msg = self.ch.ProcessCommand('notify invalid@email.com "test subject" "test body"')
        self.assertEqual(msg, 'This user does not exist')

    def test_notify_user_given_too_many_arguments_then_error_occurs(self):
        msg = self.ch.ProcessCommand('notify ta@email.com "test subject" test body')
        self.assertEqual(msg, 'Invalid number of arguments')

    def test_notify_user_given_too_few_arguments_then_error_occurs(self):
        msg = self.ch.ProcessCommand('notify ta@email.com "test subject"')
        self.assertEqual(msg, 'Invalid number of arguments')


class NotifyAsInstructor(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.super = Account.objects.create(act_email='super@email.com', role_id=4)
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        self.ta2 = Account.objects.create(act_email='ta2@email.com', role_id=1)
        self.course = Course.objects.create(course_name='course1', instructor=self.instructor)
        self.ch.currentUser = self.super
        self.ch.ProcessCommand('assign course ta course1 ta@email.com')
        self.ch.currentUser = self.instructor

    def test_notify_user_given_valid_arguments_then_notification_is_sent(self):
        msg = self.ch.ProcessCommand('notify ta@email.com "test subject" "test body"')
        self.assertEqual(msg, 'Notification email sent to ta@email.com!')

    def test_notify_user_given_ta_not_assigned_to_their_course_then_error_occurs(self):
        msg = self.ch.ProcessCommand('notify ta2@email.com "test subject" "test body"')
        self.assertEqual(msg, 'This user either does not exist, is not a TA, or is not a TA assigned to one of your courses')

    def test_notify_user_is_not_a_ta_then_error_occurs(self):
        msg = self.ch.ProcessCommand('notify admin@email.com "test subject" "test body"')
        self.assertEqual(msg, 'This user either does not exist, is not a TA, or is not a TA assigned to one of your courses')


class NotifyAsTa(TestCase):
    def setUp(self):
        self.ch = CommandHandler()
        self.super = Account.objects.create(act_email='super@email.com', role_id=4)
        self.admin = Account.objects.create(act_email='admin@email.com', role_id=3)
        self.instructor = Account.objects.create(act_email='instructor@email.com', role_id=2)
        self.ta = Account.objects.create(act_email='ta@email.com', role_id=1)
        self.ch.currentUser = self.ta

    def test_notify_user_given_valid_arguments_then_notification_is_sent(self):
        msg = self.ch.ProcessCommand('notify instuctor@email.com "test subject" "test body"')
        self.assertEqual(msg, 'TAs cannot send notifications')
