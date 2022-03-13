from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from . import util, forms
from random import choice
from markdown2 import markdown


def error_404(request, exception):
    return render(request, "encyclopedia/404.html")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)
    if content:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown(content)
        })
    raise Http404()


def search(request):
    query = request.GET.get("q")
    
    # Check if query matches the name of an encyclopedia entry
    if query in util.list_entries():
        return HttpResponseRedirect(reverse("entry", kwargs = {"title": query}))

    return render(request, "encyclopedia/index.html", {
        "heading": "Search Results",
        "entries": [entry for entry in util.list_entries() if query in entry]
    })


def new(request):
    if request.method == "POST":

        # Save submitted data as a form
        form = forms.NewEntry(request.POST)

        # Check if form data is valid
        if form.is_valid():
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")

            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs = {"title": title}))

        return render(request, "encyclopedia/newentry.html", {
            "form": form
        })
            
    return render(request, "encyclopedia/newentry.html", {
        "form": forms.NewEntry()
    })


def edit(request, title):
    if request.method == "POST":

        # Save submitted data as a form
        form = forms.EditEntry(request.POST)

        # Check if form data is valid
        if form.is_valid():
            content = form.cleaned_data.get("content")
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs = {"title": title}))

    content = util.get_entry(title)
    return render(request, "encyclopedia/newentry.html", {
        "title": title,
        "form": forms.EditEntry(initial = {"content": content}),
        "edit": True,
    })


def random(request):
    return HttpResponseRedirect(reverse("entry", kwargs = {"title": choice(util.list_entries())}))