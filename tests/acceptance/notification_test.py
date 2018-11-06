import unittest
from tests.resources.TestDataAccess import TestDataAccess
from src.Account import Account
from src.CommandHandler import CommandHandler
from src.ErrorMessages import ErrorMessages


class NotificationAsASupervisorTest(unittest.TestCase):
    def setUp(self):
        self.db = TestDataAccess()
        Account.LoadEntity(self.db)
        self.ch = CommandHandler(self.db)
        self.ch.ProcessCommand('login dfudge@school.edu dfudge12')

    def test_given_a_supervisor_tries_emailing_someone_then_email_is_sent(self):
        msg = self.ch.ProcessCommand('notify asdf@yahoo.com "subject" "body"')
        self.assertEqual(msg, 'Notification email sent to asdf@yahoo.com!')

    def test_given_a_supervisor_tries_emailing_an_invalid_email_then_email_is_sent(self):
        msg = self.ch.ProcessCommand('notify no@email.com "subject" "body"')
        self.assertEqual(msg, 'This user does not exist')

    def test_given_too_many_arguments_then_an_error_message_is_displayed(self):
        msg = self.ch.ProcessCommand('notify asdf@yahoo.com "subject" "body" invalid')
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)

    def test_given_too_few_arguments_then_an_error_message_is_displayed(self):
        msg = self.ch.ProcessCommand('notify foo@bar.com "subject"')
        self.assertEqual(msg, ErrorMessages.INVALID_NUM_OF_ARGUMENTS)


class NotificationAsATaTest(unittest.TestCase):
    def setUp(self):
        self.db = TestDataAccess()
        Account.LoadEntity(self.db)
        self.ch = CommandHandler(self.db)
        self.ch.ProcessCommand('login asdf@yahoo.com asdf1234')

    def test_given_a_ta_tries_emailing_someone_then_error_message_is_displayed(self):
        msg = self.ch.ProcessCommand('notify ta@two.com "subject" "body"')
        self.assertEqual(msg, 'TAs cannot send notifications')