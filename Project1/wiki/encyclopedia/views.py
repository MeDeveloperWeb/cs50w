from cgitb import html
import imp
from turtle import title
from django import http
from django.http import HttpResponse
from django.shortcuts import render
from markdown2 import markdown
from django import forms
from random import randint

from . import util

class CreateForm(forms.Form):
    newtitle = forms.CharField(max_length=30, label='Enter Title:')
    content = forms.CharField(widget=forms.Textarea, label='Enter the description:')



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "head": "All Pages"
    })


def entries(request, title):
    if util.get_entry(title):
        html = markdown(util.get_entry(title))
        return render(request, "encyclopedia/entries.html", {
            "title" : title,
            "html" : html
        })
    else: 
        return HttpResponse("Page Not Found")

def find(request):
    query = request.GET.get("q").lower()

    if util.get_entry(query):
        return entries(request, query)
    
    result = []
    for every in util.list_entries():
        if query in every.lower():
            result.append(every)

    return render(request, "encyclopedia/index.html", {
        "entries": result,
        "head": "Search Results"
    })


def create(request):
    if request.method == 'POST':
        print(request)
        form = CreateForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data["newtitle"]
            content = form.cleaned_data["content"]

            if util.get_entry(new_title):
                return HttpResponse("OOPS! Entry with the title already exists")

            util.save_entry(new_title, content)

            return entries(request, new_title)

    else:
        return render(request, "encyclopedia/create.html", {
            "form": CreateForm()
        })

def edit(request, title):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data["newtitle"]
            content = form.cleaned_data["content"]

            util.save_entry(new_title, content)

            return entries(request, new_title)
    else:
        return render(request, "encyclopedia/edit.html", {
                "form": CreateForm(initial={
                    "newtitle": title,
                    "content": util.get_entry(title)
                })
    })


def random(request):
    x = randint(0,len(util.list_entries()) - 1)
    return entries(request, util.list_entries()[x])
