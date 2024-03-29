from email.mime import image
from tkinter import CASCADE
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

# def validate_highest_bid(value):
#     current_bids = Bid.objects.filter(listing = Bid.listing)
#     for bid in current_bids:
#         if value <= bid:
#             raise ValidationError(f"{value} must be higher than previous value", params={'value': value})


class User(AbstractUser):
    name = models.CharField(max_length=150, blank=True, null=True)
    pass


class Category(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name

class Listing(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1200)
    starting_price = models.FloatField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True, related_name="user")
    image = models.URLField(null=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist =  models.ManyToManyField(User, blank=True, null=True, related_name="related_watchlist")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__ (self):
        return self.name

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="bidder")
    bid = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="bids")


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True, related_name='listing_comment')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_comment")
    comment = models.CharField(max_length=1200)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering= ['created_on']

    def __str__(self):
        return f'Comment {self.comment} on {self.created_on}'