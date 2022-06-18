from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entries, name="entries"),
    path("find/", views.find, name="find")
]
