from django.test import Client, TestCase
from django.utils import timezone
from network.models import User, Post


class ProfileAPITestCase(TestCase):

    def setUp(self):
        # Set datetime
        self.datetime = timezone.now()

        # Create users
        user1 = User.objects.create_user(username = "AAA", email = "AAA@outlook.com", password = "AAA", date_joined = self.datetime)
        user2 = User.objects.create_user(username = "BBB", email = "BBB@outlook.com", password = "BBB", date_joined = self.datetime)
        user3 = User.objects.create_user(username = "CCC", email = "CCC@outlook.com", password = "CCC", date_joined = self.datetime)

        # Create posts
        post1 = Post.objects.create(content = "post1", owner = user1, timestamp = self.datetime)
        post2 = Post.objects.create(content = "post2", owner = user1, timestamp = self.datetime + timezone.timedelta(days = 1))

        # Add followers to users
        user1.followers.add(user2, user3)
        user2.followers.add(user1) # user1 has 2 posts, 2 followers, 1 following 

        # Set up client to make requests
        self.client = Client()

    def test_invalid_user(self):

        # Send get request to profile
        response = self.client.get("/api/DDD")

        # Ensure that status code is 404
        self.assertEqual(response.status_code, 404)

        # Ensure that the correct json response is returned
        self.assertEqual(response.json(), {"error": "User not found."})

    def test_valid_user(self):

        # Send get request to profile
        response = self.client.get("/api/AAA?page=1")

        # Ensure that status code is 200
        self.assertEqual(response.status_code, 200)

        # Ensure that the correct json response is returned
        self.assertEqual(response.json(), {
            "id": 1,
            "username": "AAA",
            "num_posts": 2,
            "num_followers": 2,
            "num_following": 1,
            "followed": False,
            "date_joined": self.datetime.strftime("%B %Y"),
            "posts": [
                {
                    "id": 2,
                    "content": "post2",
                    "owner": "AAA",
                    "num_likes": 0,
                    "liked": False,
                    "date_posted": (self.datetime + timezone.timedelta(days = 1)).strftime("%b %d %Y, %I:%M %p"),
                },
                {
                    "id": 1,
                    "content": "post1",
                    "owner": "AAA",
                    "num_likes": 0,
                    "liked": False,
                    "date_posted": self.datetime.strftime("%b %d %Y, %I:%M %p"),                   
                }
                ],
            "page_num": 1,
            "num_pages": 1
        })

    def test_invalid_pages(self):
        # Send get request to profile with invalid page number
        response = self.client.get("/api/AAA?page=-1")

        # Ensure that status code is 404
        self.assertEqual(response.status_code, 404)

        # Ensure that the correct json response is returned
        self.assertEqual(response.json(), {"error": "Page not found."})

        # Send get request to profile with invalid page number
        response = self.client.get("/api/AAA?page=2")

        # Ensure that status code is 404
        self.assertEqual(response.status_code, 404)

        # Ensure that the correct json response is returned
        self.assertEqual(response.json(), {"error": "Page not found."})

    def test_valid_follow(self):
        # Login the user
        self.client.login(username = "AAA", password = "AAA")

        # Send put request to profile
        response = self.client.put("/api/CCC", {
            "follow": True
        },
        content_type = "application/json",
        )  

        # Ensure that status code is 204
        self.assertEqual(response.status_code, 204)
        
        # Ensure that user1 follows user3
        user1 = User.objects.get(username = "AAA")
        user3 = User.objects.get(username = "CCC")

        self.assertEqual(user1.following.count(), 2)
        self.assertIn(user3, user1.following.all())

        self.assertEqual(user3.followers.count(), 1)
        self.assertIn(user1, user3.followers.all())

    def test_unauthenticated_follow(self):
        # Send put request to profile
        response = self.client.put("/api/AAA", {
            "follow": True
        }, 
        content_type = "application/json",
        )

        # Ensure that status code is 401
        self.assertEqual(response.status_code, 401)

        # Ensure that the correct error message is returned
        self.assertEqual(response.json(), {"error": "User is not logged in."})

    def test_invalid_follow(self):
        # Login the user
        self.client.login(username = "AAA", password = "AAA")

        # Send put request to profile
        response = self.client.put("/api/AAA", {
            "follow": True
        },
        content_type = "application/json",
        )  

        # Ensure that status code is 403
        self.assertEqual(response.status_code, 403)

        # Ensure that the correct error message is returned
        self.assertEqual(response.json(), {"error": "User cannot follow himself."})

    def test_valid_unfollow(self):
        # Login the user
        self.client.login(username = "AAA", password = "AAA")

        # Send put request to profile
        response = self.client.put("/api/BBB", {
            "follow": False
        },
        content_type = "application/json",
        )  

        # Ensure that status code is 204
        self.assertEqual(response.status_code, 204)
        
        # Ensure that user1 does not follow user2
        user1 = User.objects.get(username = "AAA")
        user2 = User.objects.get(username = "BBB")

        self.assertEqual(user1.following.count(), 0)
        self.assertNotIn(user2, user1.following.all())

        self.assertEqual(user2.followers.count(), 0)
        self.assertNotIn(user1, user2.followers.all())

    def test_invalid_request(self):
        # Send post request to profile
        response = self.client.post("/api/AAA")

        # Ensure that status code is 400
        self.assertEqual(response.status_code, 400)

        # Ensure that the correct error message is returned
        self.assertEqual(response.json(), {"error": "GET or PUT request required."})