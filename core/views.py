from django.shortcuts import render, redirect
from .models import Post, PostCategory, PostComment, Feedback
from .forms import PostAddForm, CommentAddForm, FeedbackAddForm, PostAddModelForm


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
    posts = Post.objects.all() # тут получили все записи

    # В переменной posts место all пишем filter, достаем параметр, а затем достаем посты и фильтруем
    # достаем параметр (категорию)
    category = request.GET.get('category')  # GET - обращение к конкретному объекту GET (это свойство) // когда
    # прилетаю урл запросы, засовывают в гет, чтобы пользователям запроса было удобно парсить
    active_category = None

    if category:
        #достаем посты и фальтруем если получили категорию
        posts = posts.filter(category__id=category) # фильтрация по полю category (могли вместо id написать
        # title) вместо category = PostCategory(id=category)
        active_category = PostCategory.objects.get(id=category) # если у нас есть какая-то категория - мы ее достаем
        # как объект
    categories = PostCategory.objects.all() # достали категории, но их надо добавить контакст, дополняем словарь
    # новыми объектами - создали новую переменную и поместили туда словарь, ее используем теперь в рендере

    context = {
        "posts": posts,
        'categories': categories,
        'active_category': active_category
    }
    return render(request, 'posts.html', context)


def post_detail(request, post_id):
    comment_add_form = CommentAddForm() #формочка рендерится в этой фьюхе, а обрабатывается в comments_add
    post = Post.objects.get(id=post_id)
    #первый вариант
    comments = PostComment.objects.filter(post=post)

    if request.method == 'POST': # ПОД ИФ ПЕРЕНЕСЛИ ВСЕ ИЗ Comment_ADD и заменили в html ссылку на post_detail.html
        post = Post.objects.get(id=post_id)
        comment_add_form = CommentAddForm(request.POST)
        if comment_add_form.is_valid():
            data = comment_add_form.cleaned_data
        PostComment.objects.create(post=post, text=data['text'])
        return redirect('post_detail', post.id)

    context = {
        "post": post,
        'comments': comments,
        'comment_add_form': comment_add_form
    }

    return render(request, 'post_detail.html', context)


def post_add(request):

    categories = PostCategory.objects.all()
    post_add_form = PostAddModelForm()

    if request.method == "POST":
        post_add_form = PostAddModelForm(request.POST) # передаем запросу данные, эти данные должны обработаться. Когда выполнится эта строчка - мы уже знаем о том валидна эта форма
        # или нет. Как проверяется валидность:

        if post_add_form.is_valid(): #рассматриваем успешный сценарий
            data = post_add_form.cleaned_data #достали словарик
            print(data)
            #Добавляем объект в базу
            Post.objects.create(title=data['title'],
                                text=data['text'],
                                category=data['category'])
            return redirect('posts')

    context = {
        'categories' : categories,
        'post_add_form' : post_add_form
    }

    return render(request, 'post_add.html', context)


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
    feedback_add_form = FeedbackAddForm()
    if request.method == "POST":
        feedback_add_form = FeedbackAddForm(request.POST)

        if feedback_add_form.is_valid():
            data = feedback_add_form.cleaned_data
            print(data)
            Feedback.objects.create(name=data['name'], text=data['text'])
            return redirect('feedback_s')

    context = {
        'feedback_add_form' : feedback_add_form
    }

    return render(request, 'feedback_add.html', context)

def feedback_s(request):
    return render(request, 'feedback_s.html')





