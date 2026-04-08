import unittest
from app import app, db, Listing, User

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_api_listings(self):
        response = self.app.get('/api/listings')
        self.assertEqual(response.status_code, 200)

    def test_listings_page(self):
        response = self.app.get('/listings')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()