from django.contrib import admin
from django.urls import path, include
from .views import *
from .classy_views import *
# from .views import main, posts, post_detail, post_add, feedback_add, feedback_s, subscribe, unsubscribe, post_like, post_dislike, post_edit, posts_search, contacts, ContactView, SuperContactView

# создали новый список урл адресов(скопировали из blog/urls)
urlpatterns = [
    path('', main, name='main'),  # перавый параметр путь, второй - название функции, которую импортировали из .views
    path('posts', posts, name='posts'), # добавили name, его потом добавляем в ретерне функции post_add_submit
    # path('posts/search', posts_search, name='posts_search'), # добавили name, его потом добавляем в ретерне функции post_add_submit
    path('posts/search', PostSearchView.as_view(), name='posts_search'), # добавили name, его потом добавляем в ретерне функции post_add_submit
    path('posts/<int:post_id>', post_detail, name='post_detail'),
    # path('posts/add', post_add, name='post_add'),
    path('posts/add', PostAddView.as_view(), name='post_add'),

    # для редактирования поста
    path('posts/<int:post_id>/edit', post_edit, name='post_edit'),
    # path('posts/feedback_add', feedback_add, name='feedback_add'),
    path('posts/feedback_add', FeedbackView.as_view(), name='feedback_add'),
    path('posts/feedback_s', feedback_s, name='feedback_s'),

    path('subscribe/<int:profile_id>', subscribe, name='subscribe'),
    path('unsubscribe/<int:profile_id>', unsubscribe, name='unsubscribe'),

    path('like/<int:post_id>', post_like, name='post_like'),
    path('dislike/<int:post_id>', post_dislike, name='post_dislike'),


    # path('contacts', contacts, name='contacts'),
    # path('contacts', ContactView.as_view(), name='contacts'),
    path('contacts', SuperContactView.as_view(), name='contacts'),


    # path('posts/<int:post_id>/comment/add', comment_add, name='comment_add'),
    # path('posts/add_submit', post_add_submit, name='post_add_submit'), # name - прозвище урл адреса, к которому можно
    # будет обращаться из шаблона
]