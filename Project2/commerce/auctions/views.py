from dataclasses import fields
from tkinter import Label
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from pip import List

import auctions


from .models import Bid, Comments, Like, Listing, User, WatchList


class CreateListing(forms.ModelForm):
    # title = forms.CharField(label="Item name:")
    # details = forms.CharField(label="Item description:")
    # price = forms.DecimalField(label="Starting Bidding Amount:")
    # photo = forms.URLField(label="Item image URL:")

    class Meta:
        model = Listing
        exclude = ['owner_id']
        labels = {'title': _('Item name:'),
                'details':_('Item description:'),
                'price':_('Starting Bidding Amount:'),
                'photo':_('Item image URL:')
        }


def index(request):
    query = request.GET.get("q", False)
    search = []
    if query:
        search = Listing.objects.filter(Q(title=query) | Q(details__icontains=query))
        listings = {"search": search,
                    "listing": Listing.objects.exclude(Q(title=query) | Q(details__icontains=query))
        }
    else:
        listings = {"listing": Listing.objects.all()}

    return render(request, "auctions/index.html", {"listings":listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        #Adding one more error check
        #ensure field username and password are not null
        if not (username and password):
            return render(request, "auctions/register.html", {
                "message": "Please Enter all fields"
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')
def create(request):
    message = ""
    if request.method == 'POST':
        form = CreateListing(request.POST)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner_id = request.user
            obj.save()
            return HttpResponseRedirect("/")

        message = "Invalid Data"
    return render(request, "auctions/create.html", {"form" : CreateListing(),
                                                    "message": message
    })
    

def listing(request, id):
    
    def comment():
        txt = request.POST["comment_txt"]
        if not txt:
            messages.warning(request, "Comment can't be empty")
        else:
            new_cmt = Comments()
            new_cmt.view_id = Listing.objects.get(id=id)
            new_cmt.commentor_id = request.user
            new_cmt.comment_txt = txt
            new_cmt.save()
            messages.success(request, "Your Comment was added")
        return HttpResponseRedirect(reverse('listing', args=[id]))

    def like():
        if not Like.objects.filter(listing_id = Listing.objects.get(id=id), liked_by = request.user):
            new_like = Like()
            new_like.listing_id = Listing.objects.get(id=id)
            new_like.liked_by = request.user
            new_like.save()
            messages.success(request, "You liked the listing.")
        else:
            Like.objects.filter(listing_id = Listing.objects.get(id=id), liked_by = request.user).delete()
        return HttpResponseRedirect(reverse('listing', args=[id]))

    def bid(): 
        amt = float(request.POST['amt'])
        prev = Bid.objects.filter(listing_id = id)
        if amt < Listing.objects.get(id=id).price: 
            messages.warning(request, "Bidding amount must be greater than Original price.")
            return HttpResponseRedirect(reverse('listing', args=[id]))
        for bids in prev:
            if amt <= bids.bid_amt: 
                messages.warning(request, "Bidding amount must be greater than previous biddings.")
                return HttpResponseRedirect(reverse('listing', args=[id]))
        new_bid = Bid()
        new_bid.bid_amt = amt
        new_bid.bidder_id = request.user
        new_bid.listing_id = Listing.objects.get(id=id)
        new_bid.save()
        messages.success(request, "Your bid was added successfully.")
        return HttpResponseRedirect(reverse('listing', args=[id]))

    def watch():
        try:
            WatchList.objects.get(watcher = request.user.id, listing_id = id)
        except WatchList.DoesNotExist:
            watch = WatchList()
            watch.listing_id = Listing.objects.get(id=id)
            watch.watcher = request.user
            watch.save()
            messages.success(request, "Listing was added to your wishlist successfully.")
        else:
            WatchList.objects.get(watcher = request.user.id, listing_id = id).delete()
            messages.warning(request, "You removed listing from your wishlist.")
        return HttpResponseRedirect(reverse('listing', args=[id]))

    try:
        listings = {"listing": Listing.objects.get(id=id)}
    except Listing.DoesNotExist:
        return index(request)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if 'comment' in request.POST:
                return comment()
            elif 'like' in request.POST:
                return like()
            elif 'bid' in request.POST:
                return bid()
            elif 'watch' in request.POST:
                return watch() 
        else:
            messages.warning(request, "You need to login to perform this action. Please <a href='/login'>login</a>")
    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(id=id),
        "comment": Comments.objects.filter(view_id=Listing.objects.get(id=id)),
        "likes" : Like.objects.filter(listing_id=id),
        "bid" : Bid.objects.filter(listing_id=id).order_by('-bid_amt'),
        "watch": WatchList.objects.filter(watcher = request.user.id, listing_id = id)
    })


@login_required(login_url='login')
def watchlist(request):
    watch = WatchList.objects.filter(watcher=request.user.id)
    print(watch)
    listings = [d.listing_id for d in watch]
    # for each in watch:
    #     print("ok")
    #     print(each.listing_id.title)
    #     listings.append(Listing.objects.get(id=each.listing_id))

    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


