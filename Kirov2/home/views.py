from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    #return render(request, 'general.html')
    return render(request, 'home/index.html')