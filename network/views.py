import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse, resolve

from .models import User, Post
from .forms import PostForm


def index(request):
    return render(request, "network/index.html", {"form": PostForm()})


def post(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(id = post_id)

    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status = 404)

    # Return post if it is a GET request
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Check if user is logged in
    if request.user.is_authenticated:
        
        if request.method == "PUT":
            data = json.loads(request.body)
            like = data.get("like")
            if like is not None:
                if like:
                    post.likers.add(request.user)
                else:
                    post.likers.remove(request.user)

            content = data.get("content")
            if content is not None:
                postform = PostForm(dict(content = content))
                if postform.is_valid():
                    content = postform.cleaned_data.get("content")
                    if request.user == post.owner:
                        post.content = content
                        post.save()
                    else:
                        return JsonResponse({"error": "User cannot edit the post of another user."}, status = 403)
                else:
                    return JsonResponse({"error": "Invalid post content."}, status = 422)

            return HttpResponse(status = 204)

        return JsonResponse({"error": "PUT request required."}, status = 400)

    return JsonResponse({"error": "User is not logged in."}, status = 401)


def posts(request):

    if resolve(request.path_info).url_name == "following":

        # Check if user is logged in
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User is not logged in."}, status = 401)

        # Query for following posts
        posts = Post.objects.filter(owner__in = request.user.following.all()).order_by("-timestamp")

    elif resolve(request.path_info).url_name == "create":
        
        # Check if user is logged in
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User is not logged in."}, status = 401)

        if request.method == "POST":
            data = json.loads(request.body)
            content = data.get("content")
            if content is not None:
                postform = PostForm(dict(content = content))
                if postform.is_valid():
                    post = Post.objects.create(owner = request.user, **postform.cleaned_data)
                    return JsonResponse(post.serialize())

            return JsonResponse({"error": "Invalid post content."}, status = 422)

        return JsonResponse({"error": "POST request required."}, status = 400)

    else:
        # Query for posts
        posts = Post.objects.order_by("-timestamp")

    # Setup paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page") or 1
    
    return JsonResponse([post.serialize() for post in paginator.get_page(page_number)], safe = False)


def profile(request, username):

    # Query for requested user
    try:
        user = User.objects.get(username = username)

    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status = 404)

    else:

        if request.method == "GET":

            # Query for posts by the user
            user_posts = Post.objects.filter(owner = user).order_by("-timestamp")

            # Setup paginator
            paginator = Paginator(user_posts, 10)
            page_number = request.GET.get("page") or 1
            page_posts = {
                "posts": [post.serialize() for post in paginator.get_page(page_number)]
            }
            
            return JsonResponse({**user.serialize(), **page_posts})

        elif request.method == "PUT":

            # Check if user is logged in
            if not request.user.is_authenticated:
                return JsonResponse({"error": "User is not logged in."}, status = 401)

            # Check if user is trying to follow himself
            if user == request.user:
                return JsonResponse({"error": "User cannot follow himself."}, status = 403)

            data = json.loads(request.body)
            follow = data.get("follow")
            if follow is not None:
                if follow:
                    user.followers.add(request.user)
                else:
                    user.followers.remove(request.user)

            return HttpResponse(status = 204)

        else:
            return JsonResponse({"error": "GET or PUT request required."}, status = 400)


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")