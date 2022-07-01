from xml.etree.ElementTree import Comment
from django.contrib import admin
from .models import Bid, Category, Comments, Like, Listing, User
# Register your models here.

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comments)
admin.site.register(Category)
admin.site.register(Like)