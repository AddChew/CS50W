from django.test import Client, TestCase
from network.models import User


class AuthenticationAPITestCase(TestCase):
    
    def setUp(self):
        # Create user
        user = User.objects.create_user(username = "AAA", email = "AAA@outlook.com", password = "AAA")

        # Set up client to make requests
        self.client = Client()

    def test_logged_in(self):
        # Login the user
        self.client.login(username = "AAA", password = "AAA")

        # Send get request to /api/authentication
        response = self.client.get("/api/authentication")

        # Ensure that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Ensure that the correct json response is returned for logged in user
        self.assertEqual(response.json(), {"logged_in": True, "username": "AAA"})

    def test_logged_out(self):
        # Send get request to /api/authentication
        response = self.client.get("/api/authentication")

        # Ensure that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Ensure that the correct json response is returned for logged out user
        self.assertEqual(response.json(), {"logged_in": False, "username": None})

    def test_invalid_request(self):
        # Send post request to /api/authentication
        response = self.client.post("/api/authentication")

        # Ensure that the status code is 400
        self.assertEqual(response.status_code, 400)

        # Ensure that the correct error message is returned
        self.assertEqual(response.json(), {"error": "GET request required."})