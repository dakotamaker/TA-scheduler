import unittest
from tests.acceptance.labs_and_courses_test import LabsAndCoursesTest
from tests.acceptance.login_test import LoginTest
from tests.acceptance.logout_test import LogoutTest
from tests.acceptance.notification_test import *
from tests.acceptance.users_test import *
from tests.acceptance.viewing_data_test import *

suite = unittest.TestSuite()

suite.addTest(unittest.makeSuite(LabsAndCoursesTest))
suite.addTest(unittest.makeSuite(LoginTest))
suite.addTest(unittest.makeSuite(LogoutTest))
suite.addTest(unittest.makeSuite(NotificationAsASupervisorTest))
suite.addTest(unittest.makeSuite(NotificationAsATaTest))
suite.addTest(unittest.makeSuite(UsersAsASupervisorTest))
suite.addTest(unittest.makeSuite(UsersAsAnInstructorTest))
suite.addTest(unittest.makeSuite(ViewingDataAsASupervisorTest))
# suite.addTest(unittest.makeSuite(ViewingDataAsAnInstructorTest))
# suite.addTest(unittest.makeSuite(ViewingDataAsATaTest))

runner = unittest.TextTestRunner()
res = runner.run(suite)

print(res)
