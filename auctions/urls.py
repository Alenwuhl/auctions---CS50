from django.urls import path
from django.views.generic import RedirectView


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("active_listings", RedirectView.as_view(url='/', permanent=False)),
    path("create_listing", views.create_listing, name="create_listing"),
    path('listing/<int:listing_id>/', views.listing, name='listing'),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category_listings, name="category_listings"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction"),
]
