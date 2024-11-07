from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin # для аутентификации авторизации добавления коммента

from core.forms import FeedbackAddForm, PostAddModelForm
from core.models import Post, PostCategory, Subscription


class ContactView(View): # если статичных страниц много - можно пользоваться встроенными классами

    def get(self, request):
        return render(request, 'contacts.html')

# прокаченный вариант
class SuperContactView(TemplateView): # копируем, меняем html для других страниц
    template_name = 'contacts.html'


# ПЕРЕПИСАЛИ ФУНКЦИЮ feedback_add в 4 строчки КЛАССОМ
class FeedbackView(CreateView):
    """Представление для добавления обратной связи"""
    form_class = FeedbackAddForm
    template_name = 'feedback_add.html'
    success_url = '/posts/feedback_s'


class PostSearchView(ListView):
    """Представление для страницы с поиском постов"""
    queryset = Post.objects.all()
    template_name = 'posts.html' # отвечает за рендер данных
    paginate_by = 5
    extra_context = {'categories': PostCategory.objects.all()} # добавили блок с катигориями на страницу

    def get_queryset(self):
        """ Переопределяет метод get_queryset """
        queryset = super().get_queryset()
        text = self.request.GET.get('text')  # загетили параметр текст (который предварительно записали в html в name)
        if text:
            queryset = queryset.filter(Q(title__icontains=text) | Q(text__icontains=text))

        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        text = self.request.GET.get('text')

        #получили подписки
        subscriptions = None
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            subscriptions = Subscription.objects.filter(profile=profile)
        context.update({
            "subscriptions": subscriptions,
            'search_text': text
        })
        return context


# post_add вьюху тоже перепишем в ООП стиле, не забыть поправить урлы  и в post_add.html заменить post_add_form
class PostAddView(LoginRequiredMixin, CreateView):
    form_class = PostAddModelForm
    template_name = 'post_add.html'

    def post(self, request, *args, **kwargs):
        '''Переопределили метод обработки формы'''
        form = self.get_form()
        if form.is_valid():
            post = form.save(commit = False)
            profile = request.user.profile
            post.profile = profile
            post.save()

            return redirect('posts')
        else:
            return self.form_invalid(form)


