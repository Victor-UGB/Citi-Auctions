from email.mime import image
from tkinter import CASCADE
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="bidder"),
    bid = models.IntegerField()


class Listing(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1200)
    starting_price = models.FloatField(null=True, blank=True)
    bid_price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="top_bid")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True, related_name="user")
    image = models.URLField(null=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist =  models.ManyToManyField(User, blank=True, null=True, related_name="related_watchlist")

    def __str__ (self):
        return self.name




class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True, related_name='listing_comment')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_comment")
    comment = models.CharField(max_length=1200)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering= ['created_on']

    def __str__(self):
        return f'Comment {self.comment} on {self.created_on}'