from django.shortcuts import render, HttpResponse
from .models import *

# Create your views here.

def news(request):
    article = Article.objects.all().first()
    context = {'article': article}
    return render(request, 'news/news.html', context)

def detail(request, id):
    # article = Article.objects.filter(id=id).first()
    # print(article, type(article))
    # return HttpResponse(f'<h1>{article.title}</h1>')

    # пример создания новости
    # author = User.objects.get(id=request.user.id)
    # article = Article(author=author, title='Заголовок9', anouncement='Анонс9', text='Текст9')
    # article.save() #new save to DB
    # return HttpResponse(f'<h1>{article.title}</h1>')

    # пример итерирования по объектам QuerySet
    articles = Article.objects.all
    s = ''
    for article in articles:
        s +=f'<h1>{article.title}</h1><br>'
    return HttpResponse (s)
