import unittest, webtest
import app, configuration

class TestBase(unittest.TestCase):
    """
    TestBase is a base class intended for test classes. The class sets data
    needed across various test cases. Such data includes but is not limited
    to a test application used to test requests to that application.
    """

    def setUp(self):
        super(TestBase, self).setUp()

        # Initialize an application with the "TESTING" configuration.
        api = app.create_app(configuration.ConfigurationName.TESTING)
        self.app = api
        # Initialize a WebTest application that helps you create tests by
        # providing a convenient interface to run WSGI applications and verify
        # the output.
        self.webtest_app = webtest.TestApp(api)