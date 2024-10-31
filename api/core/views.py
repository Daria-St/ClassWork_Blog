from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect

from core.forms import FeedbackAddForm
from core.models import Post, PostLike, PostComment


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

def feedback(request):
    """ Обработка аякс запроса """

    if request.method == "POST":
        form = FeedbackAddForm(request.POST)

        if form.is_valid():
            form.save()

            return JsonResponse({})
        else:
            return JsonResponse({'errors': form.errors}, status=400)

def post_comments(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = PostComment.objects.filter(post=post)

    new_comments = []
    for comment in comments:
        new_comments.append({
            'text': comment.text,
            'profile': comment.profile.user.username
        })


    return JsonResponse({'comments':new_comments}, safe=False)



def film_add(request):

    #Выводим данные формы
    print(request.POST)
    #вот здесь происходит обработка формы, но ее мы делать не будем
    return redirect('vue')