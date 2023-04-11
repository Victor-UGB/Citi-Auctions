from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("listing/<int:pk>", views.listing, name="listing"),
    path("remove_from_watchlist/<int:pk>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("add_to_watchlist/<int:pk>", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid/<int:pk>", views.bid, name="bid" ),
    path("display_category", views.display_category, name="display_category"),
    path("add_comment/<int:pk>", views.add_comment, name="add_comment"),
    path("close_listing/<int:pk>", views.close_listing, name="close_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
