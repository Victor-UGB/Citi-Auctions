from django.contrib import admin
from .models import Listing, Comment, Category, Bid, User

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Bid)