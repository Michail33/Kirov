from django.contrib import admin

# Register your models here.
from .models import *

class ArticleAdmin(admin.ModelAdmin):
    ordering = ['-date', 'title', 'author']
    list_display = ['title', 'author', 'date']
    list_filter = ['title', 'author', 'date']
    list_display_links = ['date']
    #list_editable = ['title', 'author'] # не работает для полей типа ManyToMany M2M
    #readonly_fields = ['author', 'title']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['title', 'status']

# admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
