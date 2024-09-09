from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', main),
    path('posts', posts),
    path('posts/<int:post_id>', post_detail),
]
