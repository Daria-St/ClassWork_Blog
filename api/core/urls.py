from django.contrib import admin
from django.urls import path, include
from .views import *

# создали новый список урл адресов(скопировали из blog/urls)
urlpatterns = [
    path('test', test, name='api_test'),  # перавый параметр путь, второй - название функции, которую импортировали из .views

]