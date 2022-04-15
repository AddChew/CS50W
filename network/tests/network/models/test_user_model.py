from django.test import TestCase
from django.utils import timezone
from network.models import User


class UserTestCase(TestCase):

    def setUp(self):
        # Set datetime
        self.datetime = timezone.now()

        # Create users
        user1 = User.objects.create_user(username = "AAA", email = "AAA@outlook.com", password = "AAA", date_joined = self.datetime)
        user2 = User.objects.create_user(username = "BBB", email = "BBB@outlook.com", password = "BBB")
        user3 = User.objects.create_user(username = "CCC", email = "CCC@outlook.com", password = "CCC")

        # Add followers to users
        # user1 has 2 followers, 0 following
        # user2 has 1 follower, 1 following
        # user3 has 0 follower, 2 following
        user1.followers.add(user2, user3) 
        user2.followers.add(user3)

    def test_followers(self):
        user1 = User.objects.get(username = "AAA")
        user2 = User.objects.get(username = "BBB")
        user3 = User.objects.get(username = "CCC")

        # Ensure that user1 has 2 followers; user2 and user3
        self.assertEqual(user1.followers.count(), 2)
        self.assertIn(user2, user1.followers.all())
        self.assertIn(user3, user1.followers.all())

        # Ensure that user2 has 1 follower; user3
        self.assertEqual(user2.followers.count(), 1)
        self.assertIn(user3, user2.followers.all())

        # Ensure that user3 has 0 followers
        self.assertEqual(user3.followers.count(), 0)
        self.assertNotIn(user1, user3.followers.all())
        self.assertNotIn(user2, user3.followers.all())

    def test_following(self):
        user1 = User.objects.get(username = "AAA")
        user2 = User.objects.get(username = "BBB")
        user3 = User.objects.get(username = "CCC")

        # Ensure that user1 has 0 following
        self.assertEqual(user1.following.count(), 0)
        self.assertNotIn(user2, user1.following.all())
        self.assertNotIn(user3, user1.following.all())

        # Ensure that user2 has 1 following; user1
        self.assertEqual(user2.following.count(), 1)
        self.assertIn(user1, user2.following.all())

        # Ensure that user3 has 2 following; user1 and user2
        self.assertEqual(user3.following.count(), 2)
        self.assertIn(user1, user3.following.all())
        self.assertIn(user2, user3.following.all())

    def test_serialize(self):
        user1 = User.objects.get(username = "AAA")
        self.assertEqual(user1.serialize(), {
            "id": 1,
            "username": "AAA",
            "num_posts": 0,
            "num_followers": 2,
            "num_following": 0,
            "date_joined": self.datetime.strftime("%B %Y"),
        })