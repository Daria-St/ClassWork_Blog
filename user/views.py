from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import LoginForm

def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, request.POST) # передаем дополнительно request из за авторизации

        if form.is_valid():
            user = form.get_user() # доступ к объекту, который прошел валидацию
            auth_login(request, user)
            return redirect('main')

    return render(request, 'user/login.html', {'form':form})

def logout(request):
    auth_logout(request)
    return redirect('main')
