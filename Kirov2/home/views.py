from django.shortcuts import render
from django.http import HttpResponse
from .forms import DemoForm, Demo
from news.models import Article


# def index(request):
#     #return render(request, 'general.html')
#     return render(request, 'home/index.html')

def index(request):
    articles = Article.objects.all()
    s = ''
    for article in articles:
        s+= f'<h1> {article.title} </h1><br>'
    #return render(request, 'general.html')
    return HttpResponse(s)
