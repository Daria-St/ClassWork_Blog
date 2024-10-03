from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q # помогает строить более гибкий sql запрос
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView

from .models import Post, PostCategory, PostComment, Feedback, PostLike
from .forms import PostAddForm, CommentAddForm, FeedbackAddForm, PostAddModelForm
from .models import Profile, Subscription


def main(request):

    # Для вывода информации о записи ее надо сначала достать из бд с помощью орм (предварительно импортировали Post)
    post = Post.objects.all()[0] # команда достает все записи из таблицы Post, с этой конструкцией можно работать как
    # со списком, то есть можно обратиться через индекс, если хотим достать нулевой объект. Потом эту инфу надо положить
    # в какую-то переменную



    return render(request, 'main.html', {"post": post}) # передаем запрос, который пришел от пользователя и шаблон -
    # файлик main, который мы сейчас создадим, в нем будет храниться весь html нашего проекта. Создаем папку templates в корне
    # проекта ДОБАВЛЯЕМ ТРЕТИЙ АРГУМЕНТ -СЛОВАРЬ ПЕРЕМЕННАЯ:БД (context - данные, кот будут исопльзоваться в шаблоне)
    # После добвления 3го аргумента перешли в файл main.html

def posts(request):


    #Функция должна выводить все записи, которые есть по порядку
    # posts = Post.objects.all() # тут получили все записи, сортировка "всех постов"
    posts = Post.objects.prefetch_related('profile__user').all() # заменили верхнюю строчку для запросов

    # В переменной posts место all пишем filter, достаем параметр, а затем достаем посты и фильтруем
    # достаем параметр (категорию)
    category = request.GET.get('category')  # GET - обращение к конкретному объекту GET (это свойство) // когда
    # прилетаю урл запросы, засовывают в гет, чтобы пользователям запроса было удобно парсить
    author = request.GET.get('author')
    order_by = request.GET.get('order_by')
    page = request.GET.get('page', 1) # по умолчанию возвращается 1ая страница с постами


    active_category = None
    active_author = None




    if category:
        #достаем посты и фальтруем если получили категорию
        posts = posts.filter(category__id=category) # фильтрация по полю category (могли вместо id написать
        # title) вместо category = PostCategory(id=category)
        active_category = PostCategory.objects.get(id=category) # если у нас есть какая-то категория - мы ее достаем
        # как объект
    if author:
        posts = posts.filter(profile__id=author)
        active_author = Profile.objects.get(id=author)
    if order_by:
        posts = posts.order_by(order_by)

    #логика для пагинации (сколько постов на стринице, несколько страниц и тд)
    # применили метод page, передав туда page - номер страницы
    p = Paginator(posts, 5)
    page_objects = p.page(page)


    categories = PostCategory.objects.all() # достали категории, но их надо добавить контакст, дополняем словарь
    # новыми объектами - создали новую переменную и поместили туда словарь, ее используем теперь в рендере

    subscriptions = None
    if request.user.is_authenticated:
        profile = request.user.profile
        subscriptions = Subscription.objects.filter(profile=profile)

    context = {
        "posts": posts,
        'categories': categories,
        'active_category': active_category,
        'subscriptions': subscriptions,
        'active_author': active_author,
        'page_objects': page_objects
    }
    return render(request, 'posts.html', context)


def posts_search(request):
    '''Представление для поиска статей'''
    #как достать гет параметр
    posts = Post.objects.all()

    #фильтрация по слову
    text = request.GET.get('text') # загетили параметр текст (который предварительно записали в html в name)
    if text:
        posts = posts.filter(Q(title__icontains=text)|Q(text__icontains=text))

    #пагинация
    page = request.GET.get('page', 1)
    p = Paginator(posts, 5)
    page_objects = p.page(page)

    categories = PostCategory.objects.all()

    context = {
        'categories': categories,
        'page_objects': page_objects,
        'search_text': text
    }

    return render(request, 'posts.html', context)




def post_detail(request, post_id):

    #создадим пустой словарик контекста, чтобы внцтри вьюхи можно было пополнять
    context = {}

    comment_add_form = CommentAddForm() #формочка рендерится в этой фьюхе, а обрабатывается в comments_add
    post = Post.objects.get(id=post_id)
    #первый вариант
    comments = PostComment.objects.filter(post=post)

    if request.user.is_authenticated: # добавляем проверку подписки на автора
        #проверка пользователя на подписку

        is_subscribed = Subscription.objects.filter(profile=request.user.profile,
                                                    author=post.profile)
        #проверка пользователя на лайк
        is_liked = PostLike.objects.filter(profile=request.user.profile,
                                                    post=post)
        context.update({'is_subscribed': is_subscribed, 'is_liked':is_liked})


    if request.method == 'POST': # ПОД ИФ ПЕРЕНЕСЛИ ВСЕ ИЗ Comment_ADD и заменили в html ссылку на post_detail.html
        post = Post.objects.get(id=post_id)
        comment_add_form = CommentAddForm(request.POST)
        if comment_add_form.is_valid():
            data = comment_add_form.cleaned_data

        profile = request.user.profile
        PostComment.objects.create(post=post, text=data['text'], profile=profile)
        return redirect('post_detail', post.id)

    context.update({
        "post": post,
        'comments': comments,
        'comment_add_form': comment_add_form
    })

    return render(request, 'post_detail.html', context)

@login_required
def post_add(request):

    categories = PostCategory.objects.all()
    post_add_form = PostAddModelForm()

    if request.method == "POST":
        post_add_form = PostAddModelForm(request.POST) # передаем запросу данные, эти данные должны обработаться. Когда выполнится эта строчка - мы уже знаем о том валидна эта форма
        # или нет. Как проверяется валидность:

        if post_add_form.is_valid(): #рассматриваем успешный сценарий
            # data = post_add_form.cleaned_data #достали словарик
            # print(data)
            ## ДАТУ ТОЖЕ МОЖНО НЕ ДОСТАВАТЬ



            #ЭТО ВСЕ ВМЕСТО Post.objects.create (ИЗБАВЛЯЕТ ОТ РУЧНОГО СОЗДАНИЯ ОБЪЕКТА, ЭТО ПОЛЕЗНО ДЛЯ РЕДАТИРОВАНИЯ) Post.objects.create ЗАКОММЕНТИЛИ

            #создаем объект, но пока не сохраняем в базу. СОХРАНЯЕМ ФОРМУ = СОХРАНЯЕМ ОБЪЕКТ В БАЗУ
            post = post_add_form.save(commit = False)
            #достали профиль
            profile = request.user.profile # ДОБАВИЛИ СТРОЧКУ чтобы привязать пост к конкретному профайлу в create ниж
            #привязали профиль к посту и сохранили его
            post.profile = profile
            post.save()


            # #Добавляем объект в базу
            # Post.objects.create(title=data['title'],
            #                     text=data['text'],
            #                     category=data['category'],
            #                     profile=profile) # вот тут привязали профайл
            return redirect('posts')

    context = {
        'categories': categories,
        'post_add_form': post_add_form
    }

    return render(request, 'post_add.html', context)



# РЕДАКТИРОВАНИЕ ПОСТОВ
@login_required
def post_edit(request, post_id):

    post = Post.objects.get(id=post_id) # получили объект из базы

    if post.profile != request.user.profile:
        raise Http404

    form = PostAddModelForm(instance=post) # создали форму как обычно, но получили инстанс

    if request.method == 'POST':
        form = PostAddModelForm(request.POST, instance=post) # instance - привязка к старой записи
        if form.is_valid():
            # обновление объекта
            form.save()
            return redirect('post_detail', post.id)

    return render(request, 'post_edit.html', {"post_add_form":form}) # передали эту форму в контексте


# def comment_add(request, post_id):
#
#     if request.method == 'POST':
#         post = Post.objects.get(id=post_id)
#         comment_add_form = CommentAddForm(request.POST)
#         if comment_add_form.is_valid():
#             data = comment_add_form.cleaned_data
#         PostComment.objects.create(post=post, text=data['text'])
#         return redirect('post_detail', post.id)


def feedback_add(request):
    form = FeedbackAddForm()
    if request.method == "POST":
        form = FeedbackAddForm(request.POST)

        if form.is_valid():
            form.save()
            # data = feedback_add_form.cleaned_data
            # print(data)
            # Feedback.objects.create(name=data['name'], text=data['text'])
            return redirect('feedback_s')

    context = {
        'form' : form
    }

    return render(request, 'feedback_add.html', context)

# ПЕРЕПИСАЛИ ФУНКЦИЮ feedback_add в 4 строчки КЛАССОМ
class FeedbackView(CreateView):
    form_class = FeedbackAddForm
    template_name = 'feedback_add.html'
    success_url = '/posts/feedback_s'



def feedback_s(request):
    return render(request, 'feedback_s.html')


@login_required
def subscribe(request, profile_id):

    redirect_url = request.GET.get('next')

    author = Profile.objects.get(id=profile_id)
    profile = request.user.profile

    Subscription.objects.get_or_create(author=author, profile=profile)

    return redirect(redirect_url)

@login_required

# доделать вьюху с редиректом
def unsubscribe(request, profile_id):
    redirect_url = request.GET.get('next')

    author = Profile.objects.get(id=profile_id)
    profile = request.user.profile

    Subscription.objects.filter(author=author, profile=profile).delete()

    return redirect(redirect_url)


@login_required
def post_like(request, post_id):

    redirect_url = request.GET.get('next')

    post = Post.objects.get(id=post_id) # достаем пост на основе пост-айди
    profile = request.user.profile

    PostLike.objects.get_or_create(post=post, profile=profile) # get_or_create - не позволит создавать много лайков

    return redirect(redirect_url)

@login_required
def post_dislike(request, post_id):

    redirect_url = request.GET.get('next')
    post = Post.objects.get(id=post_id) # достаем пост на основе пост-айди
    profile = request.user.profile

    PostLike.objects.filter(post=post, profile=profile).delete() # get_or_create - не позволит создавать много лайков

    return redirect(redirect_url)

def contacts(request):
    return render(request, 'contacts.html')

#тоже самое с помощью классов (класс предназначен для типичной задачи)
class ContactView(View): # если статичных страниц много - можно пользоваться встроенными классами

    def get(self, request):
        return render(request, 'contacts.html')

# прокаченный вариант
class SuperContactView(TemplateView): # копируем, меняем html для других страниц
    template_name = 'contacts.html'
