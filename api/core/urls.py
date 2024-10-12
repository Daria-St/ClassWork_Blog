from django.contrib import admin
from django.urls import path, include
from .views import *

# создали новый список урл адресов(скопировали из blog/urls)
urlpatterns = [
    path('test', test, name='api_test'),  # перавый параметр путь, второй - название функции, которую импортировали из .views
    path('ajax', ajax, name='api_ajax'),

    path('posts/<int:post_id>/comments', post_comments, name='api_post_comments'),

    path('posts/<int:post_id>/like', post_like, name='api_post_like'),
    path('posts/<int:post_id>/dislike', post_dislike, name='api_post_dislike'),
    path('feedback', feedback, name='api_feedback'),

]