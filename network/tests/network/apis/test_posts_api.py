from django.test import Client, TestCase
from django.utils import timezone
from django.db.models.query import QuerySet
from network.models import User, Post


class PostsAPITestCase(TestCase):

    def setUp(self):
        # Set datetime
        self.datetime = timezone.now()

        # Create users
        user1 = User.objects.create_user(username = "AAA", email = "AAA@outlook.com", password = "AAA", date_joined = self.datetime)
        user2 = User.objects.create_user(username = "BBB", email = "BBB@outlook.com", password = "BBB", date_joined = self.datetime)
        user2.followers.add(user1)

        # Create posts
        Post.objects.create(content = "post1", owner = user2, timestamp = self.datetime)
        for i in range(1, 11):
            Post.objects.create(content = f"post{i + 1}", owner = user1, timestamp = (self.datetime + timezone.timedelta(days = i + 1)))

        self.user1_posts = [
            {
                "id": i, 
                "content": f"post{i}", 
                "owner": "AAA", 
                "num_likes": 0,
                "liked": False,
                "date_posted": (self.datetime + timezone.timedelta(days = i)).strftime("%b %d %Y, %I:%M %p")
            }
            for i in range(11, 1, -1)
        ]

        self.user2_posts = [
            {
                "id": 1, 
                "content": "post1", 
                "owner": "BBB", 
                "num_likes": 0,
                "liked": False,
                "date_posted": self.datetime.strftime("%b %d %Y, %I:%M %p")                
            }
        ]

        # Set up client to make requests
        self.client = Client()

    def test_all_posts(self):        
        # Send get request to posts for first page
        response = self.client.get("/api/posts?page=1")

        # Ensure that status code is 200
        self.assertEqual(response.status_code, 200)

        # Ensure that the correct json response is returned for first page
        self.assertEqual(response.json(), {
            "posts": self.user1_posts,
            "page_num": 1,
            "num_pages": 2
        })

        # Send get request to posts for second page
        response = self.client.get("/api/posts?page=2")

        # Ensure that status code is 200
        self.assertEqual(response.status_code, 200)

        # Ensure that the correct json response is returned for first page
        self.assertEqual(response.json(), {
            "posts": self.user2_posts,
            "page_num": 2,
            "num_pages": 2
        })

    def test_invalid_all_posts_pages(self):
        # Send get request to posts with invalid page number
        response = self.client.get("/api/posts?page=-1")

        # Ensure that status code is 404
        self.assertEqual(response.status_code, 404)

        # Ensure that the correct json response is returned
        self.assertEqual(response.json(), {"error": "Page not found."})

        # Send get request to posts with invalid page number
        response = self.client.get("/api/posts?page=3")

        # Ensure that status code is 404
        self.assertEqual(response.status_code, 404)

        # Ensure that the correct json response is returned
        self.assertEqual(response.json(), {"error": "Page not found."})

    def test_following_posts(self):
        # Login the user
        self.client.login(username = "AAA", password = "AAA")

        # Send get request to /api/posts/following
        response = self.client.get("/api/posts/following?page=1")

        # Ensure that status code is 200
        self.assertEqual(response.status_code, 200)

        # Ensure that the correct json response is returned for first page
        self.assertEqual(response.json(), {
            "posts": self.user2_posts,
            "page_num": 1,
            "num_pages": 1
        })

    def test_invalid_following_pages(self):
        # Login the user
        self.client.login(username = "AAA", password = "AAA")
        
        # Send get request to /api/posts/following with invalid page number
        response = self.client.get("/api/posts/following?page=-1")

        # Ensure that status code is 404
        self.assertEqual(response.status_code, 404)

        # Ensure that the correct json response is returned
        self.assertEqual(response.json(), {"error": "Page not found."})

        # Send get request to /api/posts/following with invalid page number
        response = self.client.get("/api/posts/following?page=2")

        # Ensure that status code is 404
        self.assertEqual(response.status_code, 404)

        # Ensure that the correct json response is returned
        self.assertEqual(response.json(), {"error": "Page not found."})

    def test_unauthenticated_following_posts(self):
        # Send get request to /api/posts/following
        response = self.client.get("/api/posts/following?page=1")

        # Ensure that status code is 401
        self.assertEqual(response.status_code, 401)

        # Ensure that the correct error message is returned
        self.assertEqual(response.json(), {"error": "User is not logged in."})

    def test_create_post(self):
        # Login the user
        self.client.login(username = "AAA", password = "AAA")

        # Send post request to /api/posts/create
        response = self.client.post("/api/posts/create", {
            "content": "post12",
        },
        content_type = "application/json",
        )

        # Ensure that status code is 200
        self.assertEqual(response.status_code, 200)

        # Ensure that the correct json response is returned for the created post
        json_response = response.json()
        json_response.pop("date_posted")

        self.assertEqual(json_response, {
            "id": 12,
            "content": "post12",
            "owner": "AAA",
            "num_likes": 0,
            "liked": False,
        })

        # Ensure that the post is correctly created in the database
        user = User.objects.get(username = "AAA")
        post = Post.objects.get(content = "post12")

        self.assertEqual(post.id, 12)
        self.assertEqual(post.content, "post12")
        self.assertEqual(post.owner, user)
        self.assertEqual(post.likers.count(), 0)

    def test_invalid_post_content(self):
        # Login the user
        self.client.login(username = "AAA", password = "AAA")

        # Send post request to /api/posts/create
        response = self.client.post("/api/posts/create", {
            "content": ""
        },
        content_type = "application/json",
        )

        # Ensure that status code is 422
        self.assertEqual(response.status_code, 422)

        # Ensure that the correct error message is returned
        self.assertEqual(response.json(), {"error": "Invalid post content."})

    def test_unauthenticated_create_post(self):
        # Send post request to /api/posts/create
        response = self.client.post("/api/posts/create", {
            "content": "post12"
        },
        content_type = "application/json",
        )

        # Ensure that status code is 401
        self.assertEqual(response.status_code, 401)

        # Ensure that the correct error message is returned
        self.assertEqual(response.json(), {"error": "User is not logged in."})

    def test_invalid_request(self):
        # Login the user
        self.client.login(username = "AAA", password = "AAA")

        # Send get request to /api/posts/create
        response = self.client.get("/api/posts/create", {
            "content": "post12"
        },
        content_type = "application/json",
        )

        # Ensure that status code is 400
        self.assertEqual(response.status_code, 400)

        # Ensure that the correct error message is returned
        self.assertEqual(response.json(), {"error": "POST request required."})