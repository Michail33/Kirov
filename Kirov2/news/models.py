from django.db import models

from django.contrib.auth.models import User
# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=80)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title', 'status']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

import datetime
class PublishedToday(models.Manager):
    def get_queryset(self):
        return super(PublishedToday).get_queryset().filter(date__gte=datetime.date.today())
class Article(models.Model):
    categories = (('E', 'Economics'),('S','Science'),('IT','IT')
    )
    #fields                                     #models.Cascade
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField('Название', max_length=50, default='')
    anouncement = models.TextField('Аннотация', max_length=250)
    text = models.TextField('Текст новости')
    date = models.DateTimeField('Дата публикации', auto_created='', auto_now=True)
    category = models.CharField(choices=categories, max_length=10, verbose_name='Категории')
    tags = models.ManyToManyField(to=Tag, blank=True)
    #slug = models.SlugField
    objects = models.Manager() # покажет только сегодняшние новости
    published = PublishedToday() # покажет только сегодняшние новости
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

