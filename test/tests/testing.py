"""Support for no database testing."""

from django.test.runner import DiscoverRunner


class DatabaselessTestRunner(DiscoverRunner):
    """A test suite runner that does not set up and tear down a database."""

    def setup_databases(self, *args, **kwargs):
        """Overrides DjangoTestSuiteRunner"""
        pass

    def teardown_databases(self, *args, **kwargs):
        """Overrides DjangoTestSuiteRunner"""
        pass
