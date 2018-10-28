import unittest
import json
import os
from src.project import Project

cwd = os.getcwd()
user_data = cwd + '/tests/resources/mock_users_data.json'
with open(user_data, 'r') as u_data:
    users = json.load(u_data)


class NotificationAsASupervisorTest(unittest.TestCase):
    def setUp(self):
        Project.command("login supervisor@one.com test")

    def test_given_a_supervisor_tries_emailing_someone_then_email_is_sent(self):
        msg = Project.command("notify instructor@one.com \"subject\" \"body\"")
        self.assertEqual(msg, "Notification sent")

    def test_given_a_supervisor_tries_emailing_an_invalid_email_then_email_is_sent(self):
        msg = Project.command("notify no@email.com \"subject\" \"body\"")
        self.assertEqual(msg, "no@email is an invalid email")

    def test_given_too_many_arguments_then_an_error_message_is_displayed(self):
        msg = Project.command("notify foo@bar.com \"subject\" \"body\" invalid")
        self.assertEqual(msg, "Too much info for one email")

    def test_given_too_few_arguments_then_an_error_message_is_displayed(self):
        msg = Project.command("notify foo@bar.com \"subject\"")
        self.assertEqual(msg, "Not enough info for an email")

    def test_given_invalid_subject_argument_then_error_is_thrown(self):
        with self.assertRaises(ValueError):
            Project.command("notify foo@bar.com 1234 \"body\"")

    def test_given_invalid_body_argument_then_error_is_thrown(self):
        with self.assertRaises(ValueError):
            Project.command("notify foo@bar.com \"subject\" 1234")


class NotificationAsATaTest(unittest.TestCase):
    def test_given_a_ta_tries_emailing_someone_then_error_message_is_displayed(self):
        Project.command("login ta@one.com test")
        msg = Project.command("notify ta@two.com \"subject\" \"body\"")
        self.assertEqual(msg, "TAs cannot send notifications")