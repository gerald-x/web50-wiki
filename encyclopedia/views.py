from django.shortcuts import render, redirect
import markdown2
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from . import util
import os
import random
import sys


class form(forms.Form):
    wiki_search = forms.CharField(widget=forms.TextInput)

class newPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput)
    body = forms.CharField(widget=forms.Textarea 
    (attrs={'placeholder': 'It should be written with markdown syntax'}))



wrong_keyword = "sorry the keyword you searched for does not exist."
existing_page = """Looks like a document with the name already exists,
    try changing the name of the document"""


def index(request):
    pages = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": pages,
        "form": form
    })


def title(request, title):
    page = util.get_entry(title)
    if page != None:
        displayed_page = markdown2.markdown(page)
        return render(request, "encyclopedia/pages.html", {
            "title": title,
            "content": displayed_page,
            "form": form
        })
    else:
        return render(request, "encyclopedia/apology.html", {
            "form": form,
            "apology_note": wrong_keyword})


def search_page(request):
    page = []
    pages = util.list_entries()
    if request.method == "POST":
        results = form(request.POST)
        if results.is_valid():
            search_results = results.cleaned_data["wiki_search"].lower()
            for i in pages:
                page.append(i.lower())
            if search_results in page:
                return title(request, search_results)
            elif any(search_results in string for string in page):
                found_matches = [string for string in page if search_results in string]
                return render(request, "encyclopedia/search_results.html", {
                    "search_results": found_matches,
                    "form": form
                })
            else:
                return render(request, "encyclopedia/apology.html", {
                    "form": form,
                    "apology_note": wrong_keyword})
    else:
        return render(request, "encyclopedia/index.html", {
            "form": form,
            "entries": pages})


def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html", {
            "newPageForm": newPageForm,
            "form": form
            }) 

    else:
        results = newPageForm(request.POST)
        if results.is_valid():
            page_head = results.cleaned_data["title"].lower()
            body = results.cleaned_data["body"]
            for i in util.list_entries():
                if i.lower() == page_head:
                    return render (request, "encyclopedia/apology.html", {
                    "apology_note": existing_page,
                    "form": form
                    })
                else:
                    util.save_entry(page_head.capitalize(), body)
                    return title(request, page_head)
                


def edit_page(request):
    if request.method == "POST":
        value = request.POST.get('edit')
        return render(request, "encyclopedia/edit_page.html", {
            "form":form,
            "page_title":value,
            "page_body":util.get_entry(value)
        })



def save_page(request):
    if request.method == "GET":
        return HttpResponseRedirect(reverse('wiki:index'))
    else:
        page_title = str(request.POST.get('head'))
        page_body = str(request.POST.get('body'))

        util.save_entry(page_title.capitalize(), page_body)
        return title(request, page_title)
        



def random_page(request):
    page = random.choice(util.list_entries())
    return title(request, page)