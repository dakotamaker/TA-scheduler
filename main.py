import unittest
from tests.acceptance.admin_test import AdminTest
from tests.acceptance.instructor_test import InstructorTest
from tests.acceptance.login_test import LoginTest
from tests.acceptance.logout_test import LogoutTest
from tests.acceptance.supervisor_test import SupervisorTest
from tests.acceptance.ta_test import TaTest

suite = unittest.TestSuite()

suite.addTest(unittest.makeSuite(AdminTest))
suite.addTest(unittest.makeSuite(InstructorTest))
suite.addTest(unittest.makeSuite(LoginTest))
suite.addTest(unittest.makeSuite(LogoutTest))
suite.addTest(unittest.makeSuite(SupervisorTest))
suite.addTest(unittest.makeSuite(TaTest))

runner = unittest.TextTestRunner()
res = runner.run(suite)

print(res)
