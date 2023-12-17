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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_object = self.object
        images = Image.objects.filter(article=current_object)
        context['images'] = images
        return context


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
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            if current_user.id != None: # проверили что не аноним
                new_article = form.save(commit=False)
                new_article.author = current_user
                new_article.save() #сохраняем в БД
                print('id новой новости ===',new_article.id) # вывод ИД новой новости
                form.save_m2m() #сохраняем теги в БД
                for img in request.FILES.getlist('image_field'):
                    Image.objects.create(article=new_article, image=img, title=img.name)
                return redirect('news_index')
    else:
        form = ArticleForm()
    return render(request, 'news/create_article.html', {'form':form})

# def index(request):
#     # пример применения пользовательского менеджера class PublishedToday(models.Manager) из news/models
#     # articles = Article.published.all()
#     # context = {'today_article':articles}
#     # it = Tag.objects.filter(title = 'IT').first()
#     # print('IT used:', it.tag_count())
#
#     reset_queries()
#     author_list = User.objects.all()
#     print(connection.queries)

from time import time
from django.core.paginator import Paginator
# def pagination(request):
#     articles = Article.objects.all()

def index(request):
    t = time()
    print(t)
    categories = Article.categories  #создали перечень категорий
    author_list = User.objects.all()  #создали перечень авторов
    if request.method == "POST":
        selected_author = int(request.POST.get('author_filter'))
        selected_category = int(request.POST.get('category_filter'))
        if selected_author == 0:  #выбраны все авторы
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(author=selected_author)
        if selected_category != 0:  #фильтруем найденные по авторам результаты по категориям
            articles = articles.filter(category__icontains=categories[selected_category-1][0])
    else:  #если страница открывется впервые
        selected_author = 0
        selected_category = 0
        articles = Article.objects.all()
    total = len(articles)
    p = Paginator(articles, 2)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {'articles': page_obj, 'author_list': author_list, 'selected_author': selected_author,
               'categories': categories,'selected_category': selected_category, 'total': total,}

    return render(request,'news/news_list.html', context)

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
