from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import AuctionListing, User, Bid, Comment
from django.contrib.auth.decorators import login_required
from decimal import Decimal


@login_required
def watchlist(request):
    user_watchlist = request.user.watchlist.all()
    paginator = Paginator(user_watchlist, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "auctions/watchlist.html",
        {"page_obj": page_obj, "empty": not user_watchlist.exists()},
    )


def categories(request):
    categories = AuctionListing.CATEGORIES
    return render(request, "auctions/categories.html", {"categories": categories})


def category_listings(request, category):
    listings = AuctionListing.objects.filter(category=category, active=True)
    paginator = Paginator(listings, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "auctions/category_listings.html",
        {"page_obj": page_obj, "category": category},
    )


def index(request):
    listings = AuctionListing.objects.filter(active=True)
    paginator = Paginator(listings, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "auctions/index.html",
        {"page_obj": page_obj, "empty": not listings.exists()},
    )


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST.get("image_url", "")
        category = request.POST.get("category", "")

        if not title or not description or not starting_bid or not category:
            messages.error(request, "All required fields must be filled.")
            return render(
                request,
                "auctions/create_listing.html",
                {"categories": AuctionListing.CATEGORIES},
            )

        try:
            starting_bid = float(starting_bid)
            if starting_bid <= 0:
                raise ValidationError("The starting bid must be a positive number.")

            listing = AuctionListing(
                title=title,
                description=description,
                starting_bid=starting_bid,
                image_url=image_url,
                category=category,
                creator=request.user,
            )
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        except ValueError:
            messages.error(request, "Starting bid must be a valid number.")
            return render(
                request,
                "auctions/create_listing.html",
                {"categories": AuctionListing.CATEGORIES},
            )
    else:
        return render(
            request,
            "auctions/create_listing.html",
            {"categories": AuctionListing.CATEGORIES},
        )


@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)

    if request.user != listing.creator:
        return redirect("listing", listing_id=listing.id)

    listing.active = False  
    highest_bid = Bid.objects.filter(listing=listing).order_by("-amount").first()
    if highest_bid:
        listing.winner = highest_bid.user
    listing.save()

    return redirect("listing", listing_id=listing.id)


def listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    highest_bid = listing.highest_bid()

    if highest_bid:
        min_bid = highest_bid.amount + Decimal("0.01")
    else:
        min_bid = listing.starting_bid

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You need to log in to perform any actions.")
            return redirect("login")

        if "add_watchlist" in request.POST:
            request.user.watchlist.add(listing)
            messages.success(request, "Added to watchlist.")

        elif "remove_watchlist" in request.POST:
            request.user.watchlist.remove(listing)
            messages.success(request, "Removed from watchlist.")

        elif "place_bid" in request.POST:
            bid_amount = float(request.POST["bid"])
            if bid_amount > min_bid:  
                bid = Bid(user=request.user, listing=listing, amount=bid_amount)
                bid.save()
                listing.current_bid = bid.amount
                listing.save()
                messages.success(request, "Your bid has been placed.")
            else:
                messages.error(
                    request,
                    f"Error: Your bid of ${bid_amount:.2f} is too low. The minimum bid is ${min_bid:.2f}.",
                )

        elif "close_auction" in request.POST and request.user == listing.creator:
            listing.active = False
            listing.save()
            messages.success(request, "The auction has been closed.")
        elif "add_comment" in request.POST:
            comment_text = request.POST.get("comment")
            if comment_text:
                comment = Comment(text=comment_text, user=request.user, listing=listing)
                comment.save()
                messages.success(request, "Your comment has been added.")
            else:
                messages.error(request, "Comment text cannot be empty.")

    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "comments": listing.comments.all(),
            "watchlist": (
                listing in request.user.watchlist.all()
                if request.user.is_authenticated
                else False
            ),
            "highest_bid": highest_bid,
            "min_bid": min_bid,
            "is_creator": request.user == listing.creator,
        },
    )
