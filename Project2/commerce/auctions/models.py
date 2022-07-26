from cProfile import label
from pyexpat import model
from time import timezone
from tkinter import CASCADE
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    def __str__(AbstractUser):
        return f"{AbstractUser.username}"
    pass
    

class Category(models.Model):
    category_name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.category_name}"

class Listing(models.Model):
    title = models.CharField(max_length=32, blank=False)
    details = models.CharField(max_length=300, blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False)
    photo = models.URLField(blank=True)
    created_at = models.DateTimeField(default=timezone.now(), editable=False)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctioner")
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="auctioner")
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bid")
    bidder_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=False)

    def __str__(self):
        return f"{self.bid_amt}"


class Comments(models.Model):
    view_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="view")
    commentor_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentor")
    comment_txt = models.CharField(max_length=300, blank=False)
    def __str__(self):
        return f"{self.comment_txt}"

class Like(models.Model):
    listing_id =  models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_obj")
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lover")
    
    def __str__(self):
        return f"{self.liked_by}"

class WatchList(models.Model):
    listing_id =  models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watch_obj")
    watcher = models.ForeignKey(User, on_delete=models.CASCADE)