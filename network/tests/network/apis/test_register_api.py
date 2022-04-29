from django.test import Client, TestCase
from network.models import User


class RegisterAPITestCase(TestCase):
    
    def setUp(self):
        # Create user
        User.objects.create_user(username = "AAA", email = "AAA@outlook.com", password = "AAA")

        # Set up client to make requests
        self.client = Client()

    def test_valid_register(self):
        # Send post request to /api/register
        response = self.client.post("/api/register", {
            "username": "BBB",
            "email": "AAA@outlook.com",
            "password": "AAA",
            "confirmation": "AAA"
        },
        content_type = "application/json",
        )

        # Ensure that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Ensure that the correct json response is returned for registered user
        self.assertEqual(response.json(), {"logged_in": True, "username": "BBB"})

        # Ensure that user is stored in the database
        try:
            User.objects.get(username = "BBB")

        except User.DoesNotExist:
            raise AssertionError("User is not registered in the database.")

        self.assertEqual(User.objects.count(), 2)

        # Ensure that we can login the user
        login_status = self.client.login(username = "BBB", password = "AAA")
        self.assertTrue(login_status)

    def test_missing_username(self):
        # Send post request to /api/register
        response = self.client.post("/api/register", {
            "username": "",
            "email": "AAA@outlook.com",
            "password": "AAA",
            "confirmation": "AAA"
        },
        content_type = "application/json",
        )

        # Ensure that the status code is 401
        self.assertEqual(response.status_code, 401)

        # Ensure that the correct error message is returned
        self.assertEqual(response.json(), {
            "username": [{"message": "This field is required.", "code": "required"}]
        })

    def test_existing_username(self):
        # Send post request to /api/register
        response = self.client.post("/api/register", {
            "username": "AAA",
            "email": "AAA@outlook.com",
            "password": "AAA",
            "confirmation": "AAA"
        },
        content_type = "application/json",
        )

        # Ensure that the status code is 401
        self.assertEqual(response.status_code, 401)

        # Ensure that the correct error message is returned
        self.assertEqual(response.json(), {
            "username": [{"message": "Username AAA already taken.", "code": "invalid"}]
        })

    def test_invalid_email(self):
        # Send post request to /api/register
        response = self.client.post("/api/register", {
            "username": "BBB",
            "email": "AAA@outlook",
            "password": "AAA",
            "confirmation": "AAA"
        },
        content_type = "application/json",
        )

        # Ensure that the status code is 401
        self.assertEqual(response.status_code, 401)

        # Ensure that the correct error message is returned
        self.assertEqual(response.json(), {
            "email": [{"message": "Enter a valid email address.", "code": "invalid"}]
        })

    def test_non_matching_passwords(self):
        # Send post request to /api/register
        response = self.client.post("/api/register", {
            "username": "BBB",
            "email": "AAA@outlook.com",
            "password": "AAA",
            "confirmation": "AAAA"
        },
        content_type = "application/json",
        )

        # Ensure that the status code is 401
        self.assertEqual(response.status_code, 401)

        # Ensure that the correct error message is returned
        self.assertEqual(response.json(), {
            "__all__": [{"message": "Passwords must match.", "code": "invalid"}]
        })

    def test_invalid_request(self):
        # Send get request to /api/register
        response = self.client.get("/api/register", {
            "username": "BBB",
            "email": "AAA@outlook.com",
            "password": "AAA",
            "confirmation": "AAA"
        },
        content_type = "application/json",
        )

        # Ensure that the status code is 400
        self.assertEqual(response.status_code, 400)

        # Ensure that the correct error message is returned
        self.assertEqual(response.json(), {"error": "POST request required."})