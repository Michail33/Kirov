from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
def index(request):
    # return HttpResponse('<h1> Главная страница! </h1>')
    return render(request, 'main/sidebar.html')
def about(request):
    # return HttpResponse('<h1> О нас </h1>')
    return render(request, 'main/about.html')
def contacts(request):
    # return HttpResponse('<h1> Контакты </h1>')
    return render(request, 'main/contacts.html')
def content(request):
    # return HttpResponse('<h1> Содержание </h1>')
    return render(request, 'main/content.html')