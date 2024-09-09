from django.db import models

class PostCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')

    class Meta: # чтобы в админке красиво отображалось название таблицы, это интерфейс
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

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


    class Meta: # чтобы в админке красиво отображалось название таблицы, это интерфейс
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.title


class PostComment(models.Model):
    text = models.TextField(max_length=1000)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='post_comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

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
