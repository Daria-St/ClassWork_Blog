from django.shortcuts import render

from .models import Post

def main(request):

    post = Post.objects.all()[0]

    return render(request, 'main.html', {"post": post})

def posts(request):

    posts = Post.objects.all()

    return render(request, 'posts.html', {'posts': posts})


def post_detail(request, post_id):

    post = Post.objects.get(id=post_id)

    return render(request, 'post_detail.html', {'post': post})