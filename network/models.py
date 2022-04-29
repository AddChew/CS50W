from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = "following", null = True, blank = True)

    def serialize(self, user):
        return {
            "id": self.id,
            "username": self.username,
            "num_posts": self.posts.count(),
            "num_followers": self.followers.count(),
            "num_following": self.following.count(),
            "followed": user in self.followers.all(),
            "date_joined": self.date_joined.strftime("%B %Y"),
        }


class Post(models.Model):
    content = models.TextField(max_length = 280)
    owner = models.ForeignKey(User, related_name = "posts", on_delete = models.CASCADE)
    likers = models.ManyToManyField(User, related_name = "likes", null = True, blank = True)
    timestamp = models.DateTimeField(default = timezone.now)

    def serialize(self, user):
        return {
            "id": self.id,
            "content": self.content,
            "owner": self.owner.username,
            "num_likes": self.likers.count(),
            "liked": user in self.likers.all(),
            "date_posted": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }

    def __str__(self):
        return f"{self.owner}: {self.content}"