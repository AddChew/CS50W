from django.test import Client, TestCase
from django.utils import timezone
from network.models import User, Post


class PostAPITestCase(TestCase):

    def setUp(self):
        # Set datetime
        self.datetime = timezone.now()

        # Create users
        user1 = User.objects.create_user(username = "AAA", email = "AAA@outlook.com", password = "AAA")
        user2 = User.objects.create_user(username = "BBB", email = "BBB@outlook.com", password = "BBB")

        # Create posts
        post1 = Post.objects.create(content = "post1", owner = user1, timestamp = self.datetime)
        post2 = Post.objects.create(content = "post2", owner = user2, timestamp = self.datetime + timezone.timedelta(days = 1))
        post2.likers.add(user1)

        # Set up client to make requests
        self.client = Client()

    def test_invalid_post(self):
        # Send get request to posts for post3
        response = self.client.get("/api/posts/3")

        # Ensure that status code is 404
        self.assertEqual(response.status_code, 404)

        # Ensure that the correct json response is returned for post3
        self.assertEqual(response.json(), {"error": "Post not found."})

    def test_valid_post(self):
        # Send get request to posts for post1
        response = self.client.get("/api/posts/1")

        # Ensure that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Ensure that the correct json response is returned for post1
        self.assertEqual(response.json(), {
            "id": 1,
            "content": "post1",
            "owner": "AAA",
            "num_likes": 0,
            "liked": False,
            "date_posted": self.datetime.strftime("%b %d %Y, %I:%M %p")
        })

        # Send get request to posts for post2
        response = self.client.get("/api/posts/2")

        # Ensure that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Ensure that the correct json response is returned for post1
        self.assertEqual(response.json(), {
            "id": 2,
            "content": "post2",
            "owner": "BBB",
            "num_likes": 1,
            "liked": False,
            "date_posted": (self.datetime + timezone.timedelta(days = 1)).strftime("%b %d %Y, %I:%M %p")
        })

    def test_unauthenticated_request(self):
        # Send put request to posts for post1
        response = self.client.put("/api/posts/1", {
            "like": True
        },
        content_type = "application/json",
        )

        # Ensure that the status code is 401
        self.assertEqual(response.status_code, 401)

        # Ensure that the correct json reponse is returned for post1
        self.assertEqual(response.json(), {"error": "User is not logged in."})

    def test_invalid_request(self):
        # Login the user
        self.client.login(username = "AAA", password = "AAA")

        # Send post request to posts for post1
        response = self.client.post("/api/posts/1", {
            "like": True
        },
        content_type = "application/json",
        )

        # Ensure that the status code is 400
        self.assertEqual(response.status_code, 400)

        # Ensure that the correct error message is returned
        self.assertEqual(response.json(), {"error": "PUT request required."})

    def test_valid_like(self):
        # Login the user
        self.client.login(username = "BBB", password = "BBB")

        # Send put request to posts for post1
        response = self.client.put("/api/posts/1", {
            "like": True
        },
        content_type = "application/json",
        )

        # Ensure that the status code is 204
        self.assertEqual(response.status_code, 204)

        # Ensure that user2 likes post1
        user2 = User.objects.get(username = "BBB")
        post1 = Post.objects.get(id = 1)

        self.assertEqual(post1.likers.count(), 1)
        self.assertIn(user2, post1.likers.all())

    def test_valid_unlike(self):
        # Login the user
        self.client.login(username = "AAA", password = "AAA")

        # Send put request to posts for post2
        response = self.client.put("/api/posts/2", {
            "like": False
        },
        content_type = "application/json",
        )

        # Ensure that the status code is 204
        self.assertEqual(response.status_code, 204)

        # Ensure that user1 no longer likes post2
        user1 = User.objects.get(username = "AAA")
        post2 = Post.objects.get(id = 2)

        self.assertEqual(post2.likers.count(), 0)
        self.assertNotIn(user1, post2.likers.all())

    def test_valid_edit(self):
        # Login the user
        self.client.login(username = "AAA", password = "AAA")

        # Send put request to posts for post1
        response = self.client.put("/api/posts/1", {
            "content": "edited post1"
        },
        content_type = "application/json",
        )

        # Ensure that the status code is 204
        self.assertEqual(response.status_code, 204)

        # Ensure that post1 is updated with its edited content
        post1 = Post.objects.get(id = 1)
        self.assertEqual(post1.content, "edited post1")

    def test_invalid_edit(self):
        # Login the user
        self.client.login(username = "AAA", password = "AAA")

        # Send put request to posts for post1
        response = self.client.put("/api/posts/1", {
            "content": ""
        },
        content_type = "application/json",
        )

        # Ensure that the status code is 422
        self.assertEqual(response.status_code, 422)

        # Ensure that the correct json response is returned
        self.assertEqual(response.json(), {"error": "Invalid post content."})

        # Ensure that post1 is not edited
        post1 = Post.objects.get(id = 1)
        self.assertNotEqual(post1.content, "")

    def test_unauthorized_edit(self):
        # Login the user
        self.client.login(username = "AAA", password = "AAA")

        # Send put request to posts for post2
        response = self.client.put("/api/posts/2", {
            "content": "AAA edited post2"
        },
        content_type = "application/json",
        )

        # Ensure that the status code is 403
        self.assertEqual(response.status_code, 403)

        # Ensure that the correct json response is returned
        self.assertEqual(response.json(), {"error": "User cannot edit the post of another user."})

        # Ensure that post2 is not edited
        post2 = Post.objects.get(id = 2)
        self.assertNotEqual(post2.content, "AAA edited post2")