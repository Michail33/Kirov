from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse, reverse_lazy
from .models import *
from django.db import connection, reset_queries
from django.views.generic import DetailView, DeleteView, UpdateView
# Create your views here.
# zan08: не понял, куда писать код (в какой файл)
from django.db import connection, reset_queries
from django.contrib.auth.decorators import login_required # человек не залогинился - отправляем на другую страницу
from .forms import *

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/news_detail.html'
    context_object_name = 'article'

class ArticleUpdateView(UpdateView):
    model = Article
    success_url =  reverse_lazy('news_index')
    template_name = 'news/create_article.html'
    fields = ['title','anouncement','text', 'tags']

class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('news_index') # именованная ссылка или абсолютная
    template_name = 'news/delete_article.html'


@login_required(login_url="/") # человек не залогинился - отправляем на другую страницу
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            current_user = request.user
            if current_user.id != None: # проверили что не аноним
                new_article = form.save(commit=False)
                new_article.author = current_user
                new_article.save() #сохраняем в БД
                print('id новой новости ===',new_article.id) # вывод ИД новой новости
                form.save_m2m()
                return redirect('news_index')
    else:
        form = ArticleForm()
    return render(request, 'news/create_article.html', {'form':form})

def index(request):
    # пример применения пользовательского менеджера class PublishedToday(models.Manager) из news/models
    # articles = Article.published.all()
    # context = {'today_article':articles}
    # it = Tag.objects.filter(title = 'IT').first()
    # print('IT used:', it.tag_count())

    reset_queries()
    author_list = User.objects.all()
    print(connection.queries)

def news(request):
    # запрос к БД со связкой по ИД
    # article = Article.objects.all().first()
    # print('Автор новости',article.title, ':', article.author.username,
    #       article.author.id, article.author.account.gender, article.author.account.nickname)
    # context = {'article': article}
    # print(request.user,request.user.id)
    # articles = Article.objects.filter(author=request.user.id)
    # print('Автор новости',articles)
        # articles = Article.objects.get(author=4)
        # print(articles.tags.all())
    # article = Article.objects.get(author=4) # тэги автора 4
    # print(article.tags.all())               # тэги автора 4
    article = Article.objects.filter(title__contains='News1').order_by('date') # icontains не учитывает регистр (не обнаружил)
    print(article)

    user_list = User.objects.filter(username__contains='m')
    print(user_list)
    for user in user_list:
        print('user ====', user, Article.objects.filter(author=user))
    # tag = Tag.objects.filter(title='IT').first() # новости тэга IT
    # tagged_news = Article.objects.filter(tags=tag) # новости тэга IT
    # print(tagged_news)                              # новости тэга IT
    context = {'article': article}
    return render(request, 'news/news.html', context)

# def detail(request, id):
#     # article = Article.objects.filter(id=id).first()
#     # print(article, type(article))
#     # return HttpResponse(f'<h1>{article.title}</h1>')
#
#     # пример создания новости
#     # author = User.objects.get(id=request.user.id)
#     # article = Article(author=author, title='Заголовок9', anouncement='Анонс9', text='Текст9')
#     # article.save() #new save to DB
#     # return HttpResponse(f'<h1>{article.title}</h1>')
#
#     # пример итерирования по объектам QuerySet
#     articles = Article.objects.all
#     s = ''
#     for article in articles:
#         s +=f'<h1>{article.title}</h1><br>'
#     return HttpResponse (s)
