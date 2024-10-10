from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect

from core.models import Post, PostLike


def test(request):

    return JsonResponse({"status": "Ok"})


def ajax(request):

    return JsonResponse({"status": "Ok", 'message': 'request'})

# скопировано из core/views
@login_required
def post_like(request, post_id):

    post = Post.objects.get(id=post_id)
    profile = request.user.profile
    PostLike.objects.get_or_create(post=post, profile=profile)
    likes = PostLike.objects.filter(post=post).count()

    return JsonResponse({"status": "Ok", 'likes': likes})

@login_required
def post_dislike(request, post_id):

    post = Post.objects.get(id=post_id)
    profile = request.user.profile
    PostLike.objects.filter(post=post, profile=profile).delete()
    likes = PostLike.objects.filter(post=post).count()

    return JsonResponse({"status": "Ok", 'likes': likes})