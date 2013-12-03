from django.http import HttpResponse
from search import main

from django.shortcuts import render

# TODO documentation
def index(request):
    return render(request, 'index.html')

# TODO documentation
# a view for python scripts
def search_request(request):
    word = request.GET.get('search')
    return HttpResponse(main(word))


# TODO documentation
# An explanation of how the parameters work:
#   - "request" is a standard Django object with various sub-objects and
#     methods. For example, to get the value of a URL parameter passed to this
#     function, you could use the code:
#         var parm_value = request.GET.get('parm_name')
#     Or to specify a default value, in the event the parameter was not set:
#         var parm_value = request.GET.get('parm_name', 'parm_default_value')
def search(request):
    return render(request, 'search.html')

def members(request):
    return render(request, 'members.html')

# TODO documentation
# An explanation of parameters, continued:
#   - "cwe" is a string that was directly captured by the regex in urls.py.
#     That is, you don't have to get() it, just use it. To print its value,
#     simply use code like this:
#         print(cwe)
def id(request, cwe):
    return render(request, 'sample_cwe.html')
    # If someone searches for a CWE ID that doesn't exist, you can have Django
    # automatically generate a 404 page by calling the code:
    #     raise Http404
    # If you want to make a pretty-looking 404 page, place it at:
    #     /var/django/kintsugi/templates/404.html
    # (the exact name is important), and Django will pick it up automagically.

