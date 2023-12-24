from unittest import case

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.utils import translation
from django.conf import settings
from django.db import connection, reset_queries
# import git
from .models import News, Product
from home.models import Demo
from news.models import Article
# zan08: не понял, куда писать код (в какой файл)
from django.db import connection, reset_queries

def index(request):
    return render(request,'main/index.html')
def examples(request):
    # пирмеры values, values_list
    # all_news = Article.objects.all().values('author', 'title')
    # for a in all_news:
    #     print(a['author'], a['title'])
    # all_news = Article.objects.all().values_list('author', 'title') # возвращает кортежи
    # for a in all_news:
    #     print(a)
    # all_news = Article.objects.all().values_list() # все записи
    # for a in all_news:
    #     print(a)
    # all_news = Article.objects.all().values_list('title')# возвращает кортежи, потребует извлекать значение сложнее
    # print(all_news)
    # all_news = Article.objects.all().values_list('title', flat=True)# возвращает кортежи, потребует извелекать значения по индексу
    # print(all_news)
    # print(all_news)
    # print(connection.queries)
    # reset_queries()
    # author_list = User.objects.all()
    # print(connection.queries)
    #print('Это модель из другого приложения', Demo)
    # value = 10
    # n1 = News ('News1', 'Text1', '07.11.2023')
    # n2 = News ('News2', 'Text2', '05.11.2023')
    #
    # l = [ n1, n2 ]
    # context = {'title': 'Страница главная',
    #            'Header1': 'Заголовок страницы',
    #            'value' : value,
    #            'number': l,
    #            }
    if request.method == 'POST':
        print('Получили POST запрос')
        print(request.POST)
        title = request.POST.get('title')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        new_product = Product(title, float(price), int(quantity))
        print('Create product: ', new_product.title, ', sum: ', new_product.amount())
    else:
        print('Получили Get запрос')
        print(request.GET)

    water = Product('Добрый минералка', 30, 2)
    chocolate = Product('Шоколадка', 80, 1)

    colors = [ 'red', 'blue', 'golden', 'black']
    context = {
        'colors': colors,
        'water': water,
        'chocolate': chocolate
    }
    # # по старому
    # article = Article.objects.get(id=1)
    # print(article.author.username)
    # select_related Один к одному, Один ко многим
    article = Article.objects.select_related('author').get(id=1)
    print(article.author.username)
    # prefetch_related многие ко многим
    # article = Article.objects.all()
    # for a in article:
    #     print(a.title, a.tags.all())
    article = Article.objects.prefetch_related('tags').all()
    print(article)
    # пример аннотирования и агрегации
    from django.db.models import Count, Avg, Max
    from django.contrib.auth.models import User
    count_articles = User.objects.annotate(Count('article', distinct=True)).order_by('article__count')
    for user in count_articles:
        print('User==', user, 'кол-во--', user.article__count)
    count_articles = User.objects.annotate(Count('article', distinct=True)).aggregate(Avg('article__count'))
    print('Среднее кол-во===', count_articles)
    max_articles_count_user = User.objects.annotate(Count('article', distinct=True)).aggregate(Max('article__count'))
    print('Максималист---', max_articles_count_user, 'User==', user)
    max_articles_count = User.objects.annotate(Count('article', distinct=True)).aggregate(Max('article__count'))
    max_articles_count_users = User.objects.annotate(Count('article', distinct=True)).filter(article__count__exact=max_articles_count['article__count__max'])
    print('Максималисты---', max_articles_count_users )
    return render(request, 'main/index.html', context)

# def get_demo(request, a, b):
#     return HttpResponse(f'You input: {a} and  {b}<br> sum a + b = {a+b}')
def get_demo(request, a, operation, b):
    match operation:
        case 'plus':
            result = int(a)+ int(b)
        case 'minus':
            result = int(a) - int(b)
        case 'multiply':
            result = int(a) * int(b)
        case 'divide':
            result = int(a) / int(b)
        case _:
            return HttpResponse(f'Неверная команда')
    return HttpResponse(f'Вы ввели: {a} и {b} <br>Результат {operation}: {result}')

def addr_calc(request, a, operation, b ): #Не работает
#     match operation:
#     case 'plus' result = int(a) + int(b)
#     case 'minus' result = int(a) - int(b)
#     case _/ return HttpResponse(f'BAD COMMAND!!!')
     return HttpResponse(f'You input: {a} and  {b}<br> {operation} = {result}')

def sidebar(request):
    return render(request, 'main/sidebar.html')
def about(request):
    return render(request, 'main/about.html')
def contacts(request):
    return render(request, 'main/contacts.html')
def content(request):
    context = {'title': 'Страница главная',
               'Header1': 'Заголовок странцицы'}
    return render(request, 'main/content.html')
def news(request):
    return render(request, 'main/news.html')
def custom_404(request, exception):
    #return render(request, 'main/news.html')
    return HttpResponse(f'Not found!!! <br><br>{exception}')

def selectlanguage(request):
    #в 25 символов входит корневой каталог + код языка из двух букв + '/'
    url = request.META.get('HTTP_REFERER')[25:]
    # print('URL:',url)
    if request.method =='POST':
        current_language = translation.get_language()
        # print('До:',current_language)
        lang = request.POST.get('language')
        translation.activate(lang)
        # print('После:',translation.get_language())
        response = HttpResponse('')
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
        # print('/'+lang+'/'+url)
        return HttpResponseRedirect('/'+lang+'/'+url)