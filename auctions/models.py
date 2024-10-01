from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    watchlist = models.ManyToManyField('AuctionListing', blank=True, related_name='watched_by')
    
    def __str__(self):
        return f"{self.username}"
    
class AuctionListing(models.Model):
    CATEGORIES = [
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics'),
        ('Home', 'Home'),
        ('Sports', 'Sports'),
        ('Books', 'Books'),
        ('Other', 'Other')
    ]
    
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=64, choices=CATEGORIES, blank=True)
    active = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings') 
    created_at = models.DateTimeField(default=timezone.now)  
    
    def highest_bid(self):
        return self.bids.order_by('-amount').first() 

    def current_price(self):
        highest_bid = self.highest_bid()
        if highest_bid:
            return highest_bid.amount
        return self.starting_bid

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey('AuctionListing', on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid of {self.amount} by {self.user.username} on {self.listing.title}"

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='comments')
    
    def __str__(self):
        return f"Comment by {self.user} on {self.listing}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlisted_items")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchlisted_by")
