from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model, authenticate
from .forms import LoginForm, RegisterForm
from .models import Profile

def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, request.POST) # передаем дополнительно request из за авторизации

        if form.is_valid(): # если юзер и пароль верные - проверяем валидность
            user = form.get_user() # доступ к объекту, который прошел валидацию
            auth_login(request, user)
            return redirect('main')

    return render(request, 'user/login.html', {'form':form})

def logout(request):
    auth_logout(request)
    return redirect('main')


def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print('Надо создать пользователя')

            #необходимо достать данные
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            User = get_user_model()
            user = User.objects.create(username=username) # создали пользователя и должны ему задать пароль. У джанги есть метод для этого:
            user.set_password(password)
            user.save()

            Profile.objects.create(user=user)

            # чтобы залогинить при регистрации
            user = authenticate(request, username=username, password=password)
            auth_login(request=request, user=user)

            return redirect('posts')

    return render(request, 'user/register.html', {'form':form})
