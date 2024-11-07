from django.shortcuts import render, redirect
from .models import Post, PostCategory, PostComment
from .forms import PostAddForm, CommentAddForm

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
    context = {
        "post": post,
        'comments': comments,
        'comment_add_form': comment_add_form
    }

    return render(request, 'post_detail.html', context)

# def post_add(request):
#
#     return render(request, 'post_add.html')
#
# def post_add_submit(request):
#     #достать данные
#     title = request.POST.get('title') # можем обращаться через квадратные скобки или метод get, но get безопаснее,
#     # тк возвращает "пусто", если ничего нет, request.POST - этой командой достаем данные из таблички,
#     # чтобы разработчику можно было с ними работать. get-запрос не умеет передавать большие данные, может делать это
#     # только в урл строке, а post-запрос скрывает под собой полезную нагрузку с инфой, которая записывается в базу
#     text = request.POST.get('text')
#
#     #добавить новый объект в бд
#     Post.objects.create(title=title, text=text)
#
#     print(title, text)
#     # print(request.POST)
#     return redirect('posts') # перекидывает на страницу с новой записью ( redirect надо добавить в импорт сверху,
#     # а в урлах добавить name='posts')

#Объединенная вьюха, не забыть убрать в урлах posts/add_submit и в post_add заменить урл post_add_submit на post_add
#Далее надо добавить во вьюху валидацию. В случае нахождения пустого поля блок кода не выполнять. А выполнять вывод
# нашей странички с доп информацией.


#---------ЗАМЕНА ЛОМАННОГО
def post_add(request):

    categories = PostCategory.objects.all()
    post_add_form = PostAddForm()

    if request.method == "POST":
        post_add_form = PostAddForm(request.POST) # передаем запросу данные, эти данные должны обработаться. Когда выполнится эта строчка - мы уже знаем о том валидна эта форма
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





# def post_add(request):
#
#     # получаем список всех категорий из БД (вверху импортировать посткатегори)
#     categories = PostCategory.objects.all()
#
#     if request.method == "POST":
#
#         title = request.POST.get('title')
#         text = request.POST.get('text')
#         category_id = request.POST.get('category') # 1) доставли id категории
#
#         if title == '' or text == '': # условия для пустой формы
#             error = 'Одно из полей пустое'
#             return render(request, 'post_add.html',{"error": error}) # и эту ошибку вывести внизу формочки post_add.html
#         # получаем категорию из базы
#         category = PostCategory.objects.get(id=category_id) # 2) достали из базы
#         #добавили объект в базу
#         Post.objects.create(title=title, text=text, category=category)  # 3) привязали категорию к записи
#         return redirect('posts')
#
#     return render(request, 'post_add.html', {'categories':categories}) #после добавления контекста переходим в
#     # post_add и добавляем цикл для прохода по категориям


#---------ЗАМЕНА ЛОМАННОГО
def comment_add(request, post_id):

    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        comment_add_form = CommentAddForm(request.POST)
        if comment_add_form.is_valid():
            data = comment_add_form.cleaned_data
        PostComment.objects.create(post=post, text=data['text'])
        return redirect('post_detail', post.id)




# def comment_add(request, post_id):
#     if request.method == 'POST':
#
#         #1й шаг - достать запись из базы по post_id
#         post= Post.objects.get(id=post_id)
#
#         #2й шаг - достать данные из формы
#         text = request.POST.get('text')   #достали данные из словаря, которые содержатся в рекуэст посте
#         PostComment.objects.create(post=post, text=text) #осздаем запись в базе
#
#         # 4й шаг - вернуться на страницу с комментарием
#         return redirect('post_detail', post.id)
#
#         #3й шаг - если все хорошо, то создать комментарий в базе



