from django.contrib import admin
from django.urls import path, include
from .views import *
from .views_rest import *

# создали новый список урл адресов(скопировали из blog/urls)
urlpatterns = [
    path('test', test, name='api_test'),  # перавый параметр путь, второй - название функции, которую импортировали из .views
    path('ajax', ajax, name='api_ajax'),

    path('posts/<int:post_id>/comments', post_comments, name='api_post_comments'),

    path('posts/<int:post_id>/like', post_like, name='api_post_like'),
    path('posts/<int:post_id>/dislike', post_dislike, name='api_post_dislike'),
    path('feedback', feedback, name='api_feedback'),
    path('rest/feedback_rest', feedback_rest, name='api_feedback_rest'),

    path('rest', test_view, name='api_test_rest'),
    path('rest/posts/<int:post_id>/comments', comments_list_rest, name='comments_list_rest'),
    path('rest/posts/<int:post_id>/comments/add', comments_add_rest, name='comments_add_rest'),

    path('rest/clicks', clicks, name='clicks')

]