from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.categories_view, name="categories"),
    path("category/<str:category_name>", views.category_view, name="category"),
    path("<str:username>/watchlist", views.watchlist_view, name="watchlist"),
    path("<str:username>/create", views.create_view, name="create"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
