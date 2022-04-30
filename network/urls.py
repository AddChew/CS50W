
from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    # API Routes
    path("api/login", views.login_user, name="login"),
    path("api/logout", views.logout_user, name="logout"),
    path("api/register", views.register_user, name="register"),
    path("api/authentication", views.authentication_status, name="authentication"),
    path("api/posts", views.posts, name="posts"),
    path("api/posts/create", views.posts, name="create"),
    path("api/posts/following", views.posts, name="following"),
    path("api/posts/<int:post_id>", views.post, name="post"),
    path("api/<str:username>", views.profile, name="profile"),
    re_path(r'^(?:.*)$', views.index, name="catch_all"),
]