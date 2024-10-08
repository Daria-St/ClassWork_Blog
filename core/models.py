from django.db import models
from user.models import Profile

class PostCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')

    class Meta: # чтобы в админке красиво отображалось название таблицы, это интерфейс
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ["title"] # сортировка категория по алфавиту от а до я

    def __str__(self): #какое значение должен возвращать объект, когда мы к нему обращаемся.
        return self.title


class Post(models.Model): # создааем таблицу и наследуем моделс
    title = models.CharField(max_length=200) # название атрибута соответствует названию поля, а значение - какой тип у
    # поля
    text = models.TextField()
    created_data = models.DateTimeField(auto_now_add=True)
    #добавляем новое поле
    category = models.ForeignKey(PostCategory,
                                 blank=True,
                                 null=True,
                                 on_delete=models.SET_NULL, # действия при удалении
                                 related_name='category_posts') # связь на уровне орм,
    # показали что хотим связаться с таблицей и передаем название этой таблицы
    # после добавления изменений нужно ввести команды мигрейшн и мигрейт и в admin.py регаем новый класс

    profile = models.ForeignKey(Profile,
                                related_name='profile_posts',
                                on_delete=models.CASCADE)


    class Meta: # чтобы в админке красиво отображалось название таблицы, это интерфейс
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ["-created_data"] # сортировка постов по новизне постов

    def __str__(self):
        return self.title


class PostComment(models.Model):
    text = models.TextField(max_length=1000)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='post_comments')
    profile = models.ForeignKey(Profile,
                                related_name='profile_comments',
                                on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ["-id"] # отсортировали комментарии, вверху новые

    def __str__(self):
        return self.text[:10]


class Feedback(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return self.name

# Таблица, в которой на кого подписываются и кто подписывается
class Subscription(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='profile_followers')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,
                               related_name='profile_following')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return self.profile.user.username


class PostLike(models.Model):
    # постлайк должен быть связан с каким-то постом
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_likes')
    created_dare = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Лайк поста'
        verbose_name_plural = 'Лайки постов'

    def __str__(self):
        return f"{self.post} - {self.profile.user}"