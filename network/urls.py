
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("api/posts", views.posts, name="posts"),
    path("api/posts/create", views.posts, name="create"),
    path("api/posts/following", views.posts, name="following"),
    path("api/posts/<int:post_id>", views.post, name="post"),
    path("api/<str:username>", views.profile, name="profile"),
]
