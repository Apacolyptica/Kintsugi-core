from django.http import HttpResponse
from search import main

from django.shortcuts import render

def index(request):
    """Renders the index page, which explains the CWE and the purpose of this
    site."""
    return render(request, 'index.html')

def search_request(request):
    """Runs a search and renders the results."""
    word = request.GET.get('search')
    return HttpResponse(main(word))


def search(request):
    """Renders the search page (to start a new search)."""
    return render(request, 'search.html')

def members(request):
    """Renders the page documenting the project members."""
    return render(request, 'members.html')

def id(request, cwe):
    """Obtains the CWE with the given ID and renders the CWE text."""
    return render(request, 'sample_cwe.html')
    # TODO
    # If someone searches for a CWE ID that doesn't exist, you can have Django
    # automatically generate a 404 page by calling the code:
    #     raise Http404
    # If you want to make a pretty-looking 404 page, place it at:
    #     /var/django/kintsugi/templates/404.html
    # (the exact name is important), and Django will pick it up automagically.

