import unittest

from server import app
import flickr_functions
from model import db, connect_to_db


class ServerTests(unittest.TestCase):
    """Flask tests for server."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)

    def test_categories(self):
        result = self.client.get("/search-results")
        self.assertIn("landmarks", result.data)

    def test_photo_info(self):
        result = self.client.get("/photo-info")
        self.assertEqual(result.status_code, 200)

    def test_user_login(self):
        """User login page test."""

        result = self.client.get("/login")

        self.assertEqual(result.status_code, 200)
        self.assertIn('<h1>Login</h1>', result.data)


class DatabaseTests(unittest.TestCase):

    def setUp(self):
        """Run these before every test."""

        # connect to testdb
        model.connect_to_db(app, "postgresql:///testdb")

        # create tables and add sample data
        model.db.create_all()
        model.example_data()

    def tearDown(self):
        """Do at end of every test."""

        model.db.session.close()
        model.db.drop_all()


if __name__ == "__main__":
    unittest.main()
