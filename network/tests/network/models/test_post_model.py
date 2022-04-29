from django.test import TestCase
from django.utils import timezone
from network.models import User, Post


class PostTestCase(TestCase):

    def setUp(self):
        # Set datetime
        self.datetime = timezone.now()

        # Create user
        user1 = User.objects.create_user(username = "AAA", email = "AAA@outlook.com", password = "AAA")

        # Create post
        post1 = Post.objects.create(content = "post1", owner = user1, timestamp = self.datetime)
        post1.likers.add(user1)

    def test_content(self):
        post = Post.objects.get(id = 1)
        self.assertEqual(post.content, "post1")

    def test_owner(self):
        user = User.objects.get(username = "AAA")
        post = Post.objects.get(id = 1)
        self.assertEqual(post.owner, user)

    def test_likers(self):
        user = User.objects.get(username = "AAA")
        post = Post.objects.get(id = 1)

        self.assertEqual(post.likers.count(), 1)
        self.assertIn(user, post.likers.all())

    def test_timestamp(self):
        post = Post.objects.get(id = 1)
        self.assertEqual(post.timestamp, self.datetime)

    def test_serialize(self):
        post = Post.objects.get(id = 1)
        user = User.objects.get(username = "AAA")
        self.assertEqual(post.serialize(user), {
            "id": 1,
            "content": "post1",
            "owner": "AAA",
            "num_likes": 1,
            "liked": True,
            "date_posted": self.datetime.strftime("%b %d %Y, %I:%M %p"),
        })                 