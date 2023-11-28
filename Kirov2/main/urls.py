"""
URL configuration for Kirov2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
#urlpatterns = [
 #   path('admin/', admin.site.urls),
#]
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('product/<int:a>/detail/<int:b>/', views.get_demo),
    path('calc/<int:a>/<slug:operation>/<int:b>/', views.addr_calc),
    path('about/', views.about, name='about'),
    path('news/', views.news, name='news'),
    path('contacts/', views.contacts, name='contact'),
    path('content/', views.content, name='content'),
    path('sidebar/', views.sidebar, name='sidebar'),
]