from django.test import Client, TestCase
from network.models import User


class LoginAPITestCase(TestCase):
    
    def setUp(self):
        # Create user
        user = User.objects.create_user(username = "AAA", email = "AAA@outlook.com", password = "AAA")

        # Set up client to make requests
        self.client = Client()

    def test_valid_login(self):
        # Send post request to /api/login
        response = self.client.post("/api/login", {
            "username": "AAA",
            "password": "AAA"
        },
        content_type = "application/json",
        )

        # Ensure that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Ensure that the correct json response is returned for logged in user
        self.assertEqual(response.json(), {"logged_in": True, "username": "AAA"})

    def test_invalid_username(self):
        # Send post request to /api/login
        response = self.client.post("/api/login", {
            "username": "",
            "password": "AAA"
        },
        content_type = "application/json",
        )

        # Ensure that the status code is 401
        self.assertEqual(response.status_code, 401)

        # Ensure that the correct error message is returned for invalid username
        self.assertEqual(response.json(), {"error": "Invalid username and/or password."})

    def test_invalid_password(self):
        # Send post request to /api/login
        response = self.client.post("/api/login", {
            "username": "AAA",
            "password": ""
        },
        content_type = "application/json",
        )

        # Ensure that the status code is 401
        self.assertEqual(response.status_code, 401)

        # Ensure that the correct error message is returned for invalid password
        self.assertEqual(response.json(), {"error": "Invalid username and/or password."})
    
    def test_incorrect_username(self):
        # Send post request to /api/login
        response = self.client.post("/api/login", {
            "username": "BBB",
            "password": "AAA"
        },
        content_type = "application/json",
        )

        # Ensure that the status code is 401
        self.assertEqual(response.status_code, 401)

        # Ensure that the correct error message is returned for incorrect username
        self.assertEqual(response.json(), {"error": "Invalid username and/or password."})

    def test_incorrect_password(self):
        # Send post request to /api/login
        response = self.client.post("/api/login", {
            "username": "AAA",
            "password": "BBB"
        },
        content_type = "application/json",
        )

        # Ensure that the status code is 401
        self.assertEqual(response.status_code, 401)

        # Ensure that the correct error message is returned for incorrect password
        self.assertEqual(response.json(), {"error": "Invalid username and/or password."})

    def test_invalid_request(self):
        # Send get request to /api/login
        response = self.client.get("/api/login", {
            "username": "AAA",
            "password": "AAA"
        },
        content_type = "application/json",
        )

        # Ensure that the status code is 400
        self.assertEqual(response.status_code, 400)

        # Ensure that the correct error message is returned
        self.assertEqual(response.json(), {"error": "POST request required."})