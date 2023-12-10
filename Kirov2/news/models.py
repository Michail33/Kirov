from django.db import models

from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db.models import Count

# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=80)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.title

# обкатка, пока не работает
    # def tag_count(self):
    #     print('!!!!!!!!!!!!!!!!!!!', self)
    #     count = self.objects.annotate(tag_count=Count('article'))
    #     print(count)
    #     return object.tag_count

    class Meta:
        ordering = ['title', 'status']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

import datetime
class PublishedToday(models.Manager):
    def get_queryset(self):
        return super(PublishedToday).get_queryset().filter(date__gte=datetime.date.today())
class Article(models.Model):
    categories = (('E', 'Economics'), ('S', 'Science'), ('IT', 'IT'))
    #fields                                     #models.Cascade
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField('Название', max_length=50, default='')
    anouncement = models.TextField('Аннотация', max_length=250)
    text = models.TextField('Текст новости')
    date = models.DateTimeField('Дата публикации', auto_created='', auto_now=True)
    category = models.CharField(choices=categories, max_length=10, verbose_name='Категории')
    tags = models.ManyToManyField(to=Tag, blank=True)
    slug = models.SlugField(unique=True)  # самозаполняемое поле, unique=True дает ошибку при миграции в уже созданную таблицу
    objects = models.Manager()  # покажет только сегодняшние новости
    published = PublishedToday()  # покажет только сегодняшние новости

    #методы моделей
    def __str__(self):
        return (f'Новость: {self.title} от {str(self.date) [:16]}')

    def get_absolute_url(self):
        return f'news/show/{self.id}'

    def tag_list(self):
        s = ''
        for t in self.tags.objects.all():
            s += t.title+''
            return s

    # метаданные  модели
    class Meta:
        ordering = ['title', 'date']
        verbose_name = 'Новост'
        verbose_name_plural = 'Новостииии'

class Image(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='article_images/', default='default.jpg')

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image is not None:
            return mark_safe(f'<img src="{self.image.url}" height="50px" width="auto" />')
        else:
            return 'no image'


