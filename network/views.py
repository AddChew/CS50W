import json
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import resolve
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import User, Post
from .forms import LoginForm, RegisterForm, PostForm


@ensure_csrf_cookie
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
        return JsonResponse(post.serialize(request.user))

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
                    return JsonResponse(post.serialize(request.user))

            return JsonResponse({"error": "Invalid post content."}, status = 422)

        return JsonResponse({"error": "POST request required."}, status = 400)

    else:
        # Query for posts
        posts = Post.objects.order_by("-timestamp")

    # Setup paginator
    paginator = Paginator(posts, 10)
    page_num = int(request.GET.get("page") or 1)
    num_pages = paginator.num_pages

    # Ensure that page_num is valid
    if page_num > num_pages or page_num < 1:
        return JsonResponse({"error": "Page not found."}, status = 404)
    
    return JsonResponse({
        "posts": [post.serialize(request.user) for post in paginator.get_page(page_num)],
        "page_num": page_num,
        "num_pages": num_pages,
    })


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
            page_num = int(request.GET.get("page") or 1)
            num_pages = paginator.num_pages

            # Ensure that page_num is valid
            if page_num > num_pages or page_num < 1:
                return JsonResponse({"error": "Page not found."}, status = 404)

            page_posts = {
                "posts": [post.serialize(request.user) for post in paginator.get_page(page_num)],
                "page_num": page_num,
                "num_pages": num_pages,
            }
            
            return JsonResponse({**user.serialize(request.user), **page_posts})

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


def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        loginform = LoginForm(data)

        if loginform.is_valid():

            # Attempt to sign user in
            user = authenticate(request, **loginform.cleaned_data)

            # Check if authentication is successful
            if user is not None:
                login(request, user)
                return JsonResponse({"logged_in": True, "username": request.user.username})

        return JsonResponse({"error": "Invalid username and/or password."}, status = 401)

    return JsonResponse({"error": "POST request required."}, status = 400)


def logout_user(request):
    if request.method == "GET":
        logout(request)
        return JsonResponse({"logged_in": False, "username": None})

    return JsonResponse({"error": "GET request required."}, status = 400)


def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        registerform = RegisterForm(data)

        if registerform.is_valid():

            # Pop confirmation from cleaned data
            registerform.cleaned_data.pop("confirmation")

            # Create user
            user = User.objects.create_user(**registerform.cleaned_data)

            # Login user
            login(request, user)

            return JsonResponse({"logged_in": True, "username": request.user.username})

        return JsonResponse(registerform.errors.get_json_data(), status = 401)

    return JsonResponse({"error": "POST request required."}, status = 400)
    

def authentication_status(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return JsonResponse({"logged_in": True, "username": request.user.username})
        return JsonResponse({"logged_in": False, "username": None})

    return JsonResponse({"error": "GET request required."}, status = 400)


# def login_view(request):
#     if request.method == "POST":

#         loginform = LoginForm(request.POST)
#         if loginform.is_valid():

#         # Attempt to sign user in
#             username = request.POST["username"]
#             password = request.POST["password"]
#             user = authenticate(request, username=username, password=password)

#             # Check if authentication successful
#             if user is not None:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse("index"))
#             else:
#                 return render(request, "network/login.html", {
#                     "message": "Invalid username and/or password."
#                 })
#         return render(request, "network/login.html", {"loginform": loginform})
#     else:
#         return render(request, "network/login.html", {"loginform": LoginForm()})


# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("index"))


# def register(request):
#     if request.method == "POST":
#         registerform = RegisterForm(request.POST)
#         if registerform.is_valid():
#             print("Valid!")
#         print(registerform.errors.as_json())
#         return render(request, "network/register.html", {"registerform": registerform})
        # username = request.POST["username"]
        # email = request.POST["email"]

        # # Ensure password matches confirmation
        # password = request.POST["password"]
        # confirmation = request.POST["confirmation"]
        # if password != confirmation:
        #     return render(request, "network/register.html", {
        #         "message": "Passwords must match."
        #     })

        # # Attempt to create new user
        # try:
        #     user = User.objects.create_user(username, email, password)
        #     user.save()
        # except IntegrityError:
        #     return render(request, "network/register.html", {
        #         "message": "Username already taken."
        #     })
        # login(request, user)
        # return HttpResponseRedirect(reverse("index"))
    # else:
    #     return render(request, "network/register.html", {"registerform": RegisterForm()})