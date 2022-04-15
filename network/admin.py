from django.contrib import admin
from .models import User, Post


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "num_posts", "num_followers", "num_following", "num_likes", "is_active")
    list_filter = ("is_active",)
    search_fields = ("username__icontains", "email__icontains")

    def num_posts(self, obj):
        return obj.posts.count()

    def num_followers(self, obj):
        return obj.followers.count()

    def num_following(self, obj):
        return obj.following.count()

    def num_likes(self, obj):
        return obj.likes.count()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("content", "owner", "num_likes", "timestamp")
    search_fields = ("content__icontains", "owner__username__icontains", "owner__email__icontains")

    def num_likes(self, obj):
        return obj.likers.count()