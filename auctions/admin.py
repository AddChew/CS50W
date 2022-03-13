from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_active")
    list_filter = ("is_active",)
    search_fields = ("username__icontains", "email__icontains")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name__icontains",)


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ("price", "item", "owner")
    search_fields = ("item__title__icontains", "owner__username__icontains", "owner__email__icontains")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "item", "owner", "date")
    search_fields = ("item__title__icontains", "owner__username__icontains", "owner__email__icontains")


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "start_price", "get_winning_bid", "get_categories", "owner", "date", "is_active")
    list_filter = ("is_active",)
    search_fields = (
        "title__icontains",
        "owner__username__icontains", 
        "owner__email__icontains",
        )

    @admin.display(description="categories")
    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    @admin.display(description="Winning Bid")
    def get_winning_bid(self, obj):
        return obj.bids.last()