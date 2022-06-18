from cgitb import html
from django.http import HttpResponse
from django.shortcuts import render
from markdown2 import markdown_path
from django import forms

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "head": "All Pages"
    })

def entries(request, title):
    html = markdown_path("entries/" + title + ".md")
    return render(request, "encyclopedia/entries.html", {
        "title" : title,
        "html" : html
    })

def find(request):
    query = request.GET.get("q").lower()

    if query in [x.lower() for x in util.list_entries()]:
        return entries(request, query)
    
    result = []
    for every in util.list_entries():
        if query in every.lower():
            result.append(every)

    return render(request, "encyclopedia/index.html", {
        "entries": result,
        "head": "Search Results"
    })
