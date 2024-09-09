from django.contrib import admin
from django.urls import path, include

from .views import main, posts, post_detail, post_add, feedback_add, feedback_s

# создали новый список урл адресов(скопировали из blog/urls)
urlpatterns = [
    path('', main, name='main'),  # перавый параметр путь, второй - название функции, которую импортировали из .views
    path('posts', posts, name='posts'), # добавили name, его потом добавляем в ретерне функции post_add_submit
    path('posts/<int:post_id>', post_detail, name='post_detail'),
    path('posts/add', post_add, name='post_add'),
    path('posts/feedback_add', feedback_add, name='feedback_add'),
    path('posts/feedback_s', feedback_s, name='feedback_s')
    # path('posts/<int:post_id>/comment/add', comment_add, name='comment_add'),
    # path('posts/add_submit', post_add_submit, name='post_add_submit'), # name - прозвище урл адреса, к которому можно
    # будет обращаться из шаблона
]