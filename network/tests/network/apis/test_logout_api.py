from django.test import Client, TestCase
from network.models import User


class LogoutAPITestCase(TestCase):
    
    def setUp(self):
        # Create user
        user = User.objects.create_user(username = "AAA", email = "AAA@outlook.com", password = "AAA")

        # Set up client to make requests
        self.client = Client()

    def test_valid_logout(self):
        # Send get request to /api/logout
        response = self.client.get("/api/logout")

        # Ensure that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Ensure that the correct json response is returned for logged out user
        self.assertEqual(response.json(), {"logged_in": False, "username": None})

    def test_invalid_request(self):
        # Send post request to /api/login
        response = self.client.post("/api/logout")

        # Ensure that the status code is 400
        self.assertEqual(response.status_code, 400)

        # Ensure that the correct error message is returned
        self.assertEqual(response.json(), {"error": "GET request required."})