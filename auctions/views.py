from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import *


def error_404(request, exception):
    return render(request, "auctions/404.html")


def index(request):
    # Get active listings
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {"listings": listings})


def categories_view(request):
    # Get categories
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})


def category_view(request, category_name):
    # Check if category is valid
    if not Category.objects.filter(name=category_name).exists():
        raise Http404

    # Get active listings from selected category
    listings = Listing.objects.filter(categories__name=category_name, is_active=True)
    return render(request, "auctions/index.html", {"category_name": category_name, "listings": listings})


@login_required
def watchlist_view(request, username):
    # Check if username is valid
    if not User.objects.filter(username=username).exists():
        raise Http404

    # Get listings in user watchlist
    listings = request.user.watchlists.all()
    return render(request, "auctions/index.html", {"listings": listings, "watchlist": True})


@login_required()
def create_view(request, username):
    # Check if username is valid
    if not User.objects.filter(username=username).exists():
        raise Http404

    form = CreateListingForm()

    if request.method == "POST":
        form = CreateListingForm(request.POST)

        if form.is_valid():

            categories = form.cleaned_data.pop("categories")
            listing = Listing.objects.create(owner=request.user, **form.cleaned_data)
            listing.categories.set(categories)
            
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

    return render(request, "auctions/create.html", {"form": form})


def listing_view(request, listing_id):
    # Check if listing exists
    try:
        listing = Listing.objects.get(id=listing_id)

    except Listing.DoesNotExist:
        raise Http404

    bidform = BidForm()
    commentform = CommentForm()
    message, alert_class = None, "alert-success"

    if request.method == "POST":

        btnform = ButtonForm(request.POST)
        commentform = CommentForm(request.POST)

        if btnform.is_valid():
            commentform = CommentForm()
            btn = btnform.cleaned_data.get("btn")

            if btn == "Place Bid":
                bidform = BidForm(request.POST)
                message, alert_class = "An error occurred while processing your request.", "alert-danger"

                if bidform.is_valid():
                    price = bidform.cleaned_data.get("price")
                    highest_bid = listing.bids.last()
                    highest_bid = highest_bid.price if highest_bid else 0
                    message = "Please ensure that your bid is greater than the current bid."

                    if price >= listing.start_price and price > highest_bid:
                        bidform = BidForm()
                        bid = Bid(price = price, item = listing, owner = request.user)
                        bid.save()
                        message = "Your bid has been placed successfully."
                        alert_class = "alert-success"

            if btn == "Add to Watchlist":
                message = "Listing has been added to your watchlist successfully."
                listing.watchers.add(request.user)

            if btn == "Remove from Watchlist":
                message = "Listing has been removed from your watchlist successfully."
                listing.watchers.remove(request.user)

            if btn == "Close Auction":
                message = "Your auction has been closed successfully."
                listing.is_active = False
                listing.save()

        if commentform.is_valid():
            comment = Comment(item = listing, owner = request.user, **commentform.cleaned_data)
            comment.save()
            commentform = CommentForm()

    return render(request, "auctions/listing.html", {
        "listing": listing, "bidform": bidform, "commentform": commentform,
        "message": message, "alert_class": alert_class,
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")