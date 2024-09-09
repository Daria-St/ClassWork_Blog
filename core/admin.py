from django.contrib import admin

# Register your models here.

from .models import Post, PostCategory, PostComment, Feedback
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(PostComment)
admin.site.register(Feedback)