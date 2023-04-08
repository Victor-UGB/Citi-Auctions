from xml.etree.ElementTree import Comment
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import NewListingForm, NewCommentForm, NewBidForm
from .models import Category, User, Listing, Comment, Bid



def index(request):
    # listings = get_object_or_404(Listing)
    all_category = Category.objects.all()
    return render(request, "auctions/index.html", {
        'listings' : Listing.objects.filter(is_active=True),
        'user' : request.user,
        'categories' : all_category
        # 'comments' : listings.comments.all()
    })

def add_listing(request):
    # if the user request method is POST
    if request.method == "POST":
        # if user is logged in
        # initialize form and check for its validity
        user = request.user
        form = NewListingForm(request.POST)
        # Get the starting_price input from form
        price = form.fields["starting_price"]

        form_price = request.POST['starting_price']
        # Bind starting_price to a new bids object
        bid = Bid(bid= int(form_price))  
        bid.save()
        print(f'printing bid... {bid.bid}')
        # Rewrite the starting_price of POST form to be an instance of the Bid object 

        # request.POST['starting_price'] = bid
        user_form = request.POST

        new_form = NewListingForm(user_form)
        
        print(form)
        print(new_form)
        print(f"This is the new bid: {form_price}")
        
        if new_form.is_valid():
            full_form = new_form.save(commit=False)
            full_form.bid_price = bid
            full_form.save()
            return HttpResponseRedirect(reverse('index'))
        return render(request, "auctions/add_listing.html", {
            'form' : NewListingForm(),
            'message' : "There is an error"
    })

    return render(request, "auctions/add_listing.html", {
        'form' : NewListingForm()
    })

def add_comment(request, pk):
    user = request.user
    listing = get_object_or_404(Listing, pk=pk)
    comment_form = NewCommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.author = user
        comment.listing = listing
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=(pk, )))



def display_category(request):

    if request.method == "POST":
    #get category input
        all_categories = Category.objects.all()
        category_from_form = request.POST["categories"]
        category = Category.objects.get(category_name = category_from_form)
        category_collection  = Listing.objects.filter(is_active = True, category = category)
        return render(request, "auctions/index.html", {
            'listings' : category_collection,
            'categories' : all_categories,         
        })

def bid(request, pk):
    # get listing and user who placed bid
    listing = get_object_or_404(Listing, pk=pk)
    user = request.user

    # check that request method is POST
    if request.method == "POST":

        #get bid form and pass  request to check validity
        bid_form = NewBidForm(request.POST)
        print(bid_form)
        
        # if valid save
        if bid_form.is_valid():
            bid = bid_form.save(commit=False)
            bid.bidder = user
            bid.listing = listing
            bid.save()
            return HttpResponseRedirect(reverse, "listing", args=(pk,))
    
        return render(request, "auctions/index.html")




def listing(request, pk):
    #get the listing by id
    listing = get_object_or_404(Listing, pk=pk)
    listing_in_watchlist = request.user in listing.watchlist.all()
    comments_in_listing = Comment.objects.filter(listing=listing)

    # top_bid = Bid.objects.filter(listing=listing)
    #return html pagee with the listing information
    return render(request, 'auctions/listing.html', {
        'listing' : listing,
        'listing_in_watchlist' : listing_in_watchlist,
        'comments' : comments_in_listing,
        'new_comment_form' : NewCommentForm()
    })




def remove_from_watchlist(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    user = request.user
    listing.watchlist.remove(user)

    return HttpResponseRedirect(reverse("listing", args=(pk, )))


def add_to_watchlist(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    user = request.user
    print(user)
    print(request)
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(pk, )))


def watchlist(request):
    user = request.user
    listing_in_watchlist = user.related_watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings" : listing_in_watchlist
    })


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
