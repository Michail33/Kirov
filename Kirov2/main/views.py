from unittest import case

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from .models import News, Product
from home.models import Demo
def index(request):
    print('Это модель из другого приложения', Demo)
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
    return render(request, 'main/index.html', context)

def get_demo(request, a, b):
    return HttpResponse(f'You input: {a} and  {b}<br> sum a + b = {a+b}')

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