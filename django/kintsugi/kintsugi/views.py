# from django.http import HttpResponse
from django.shortcuts import render

def index(request):
#    return HttpResponse("Hello, world. Future Kintsugi index goes here.")
    return render(request, 'index.html')

