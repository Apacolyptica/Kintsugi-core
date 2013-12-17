#!/usr/bin/env python3
"""
Views for the CWE Explorer (kintsugi) project.
"""
from django.http import HttpResponse
from django.template import RequestContext, loader

from wholetest import run_wholetest
from result_page import run_result_page

from django.shortcuts import render

def index(request):
    """Renders the index page, which explains the CWE and the purpose of this
    site."""
    return render(request, 'index.html')

def search_request(request):
    """Runs a search and renders the results."""

    """obtain the search phrase/word from the form"""
    word = request.GET.get('search')

    """run the query script to find matching results"""
    ugly_results = run_wholetest(str(word))

    """load the template for search results"""
    template = loader.get_template('search.html')

    """set the request context with the variable to be sent to the template"""
    context = RequestContext(request, { 'ugly_results': ugly_results, })

    """render the HTML template and pass it the variable"""
    return HttpResponse(template.render(context))


##def search(request):
 ##   """Renders the search page (to start a new search)."""
  ##  return render(request, 'search.html')

def members(request):
    """Renders the page documenting the project members."""
    return render(request, 'members.html')

def id(request, cwe):
    """Obtains the CWE with the given ID and renders the CWE text."""
    cwe_result = run_result_page(cwe)

    """load the template for search results"""
    template = loader.get_template('cwe.html')

    """set the request context with the variable to be sent to the template"""
    context = RequestContext(request, { 'cwe_result': cwe_result, })

    """render the HTML template and pass it the variable"""
    return HttpResponse(template.render(context))
    # TODO
    # If someone searches for a CWE ID that doesn't exist, you can have Django
    # automatically generate a 404 page by calling the code:
    #     raise Http404
    # If you want to make a pretty-looking 404 page, place it at:
    #     /var/django/kintsugi/templates/404.html
    # (the exact name is important), and Django will pick it up automagically.

