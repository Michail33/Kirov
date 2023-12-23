from django.shortcuts import render, HttpResponse, redirect
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import AccountUpdateForm, UserUpdateForm

def profile(request):
    return render(request, 'users/profile.html' )
    # return render(request, 'users/user_panel.html')
def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print('Сообщение отправлено', form.cleaned_data)
            user = form.save()  #появляется новый пользователь
            group = Group.objects.get(name='Authors')
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # не аутентифицируется нужно доделать
            user = authenticate(username=username, password=password)  #аутентификация пользователя
            messages.success(request, f'{username} был зарегистрирован!')
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)

def profile_update(request):
    user = request.user
    account = Account.objects.get(user=user)
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        account_form = AccountUpdateForm(request.POST, request.FILES, instance=account)
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            messages.success(request,"Профиль успешно обновлен")
            return redirect('profile')
        else:
            pass
    else:
        context = {'account_form':AccountUpdateForm(instance=account),
                   'user_form':UserUpdateForm(instance=user)}
    return render(request,'users/edit_profile.html',context)



def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print('Сообщение отправлено', form.cleaned_data)
        else:
            print(form.errors)
    else:
        form = ContactForm()
        form.name = 'Любимый клиент'
    context={'form': form}
    return render(request, 'users/contact_page.html', context)

# Create your views here.
def index(request):
    print(request.user, request.user.id)
    user_acc = Account.objects.get(user=request.user)
    # get - запрос в БД
    print(user_acc.birthdate, user_acc.nickname, user_acc.gender)

    #можно так, но дольше
    #print(Account.objects.get(user=request.user).birthdate, user_acc.nickname, user_acc.gender)
    return HttpResponse('Приложение Юзерзz')
