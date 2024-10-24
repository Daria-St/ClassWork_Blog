from rest_framework.response import Response
from rest_framework.decorators import api_view

from core.models import PostComment, Post, Feedback
from .serialaizers import CommentsSerialaizer, FeedbackSerialaizer


@api_view(['GET'])
def test_view(request):
    return Response({'message': 'Hello'})


@api_view(['GET'])
def comments_list_rest(request, post_id): # логика, которая будет использовать сериалайзеры и применять в json
    comments =PostComment.objects.filter(post__id=post_id)
    serialaizer = CommentsSerialaizer(comments, many=True) #many - ожидаем получить список комментариев, то есть несколько словарей
    return Response({'comments':serialaizer.data}) # data содержмт в себе json, который получается

@api_view(['POST'])
def comments_add_rest(request, post_id):
    #достали
    post = Post.objects.get(id=post_id)
    profile = request.user.profile
    # проверили на валидацию
    serialaizer = CommentsSerialaizer(data=request.data)
    serialaizer.is_valid(raise_exception=True)

    serialaizer.save(post=post, profile=profile)

    return Response(status=200)

@api_view(['POST'])
def feedback_rest(request):

    serialaizer = FeedbackSerialaizer(data=request.data)
    serialaizer.is_valid(raise_exception=True)

    serialaizer.save()

    return Response(status=200)

@api_view(['GET'])
def clicks(request):
    return Response({'clicks': 100})