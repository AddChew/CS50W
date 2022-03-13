from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=50)
    desc = models.TextField(max_length=150, blank=True)
    start_price = models.FloatField(default=0, validators=[MinValueValidator(0, "Start price must be greater than or equal to 0.")])

    url = models.CharField(max_length=250, blank=True)
    categories = models.ManyToManyField(Category, related_name="listings")
    is_active = models.BooleanField(default=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    watchers = models.ManyToManyField(User, related_name="watchlists", null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Bid(models.Model):
    price = models.FloatField(default=0)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.owner}: ${self.price}"


class Comment(models.Model):
    post = models.TextField(max_length=250)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner}: {self.post}"