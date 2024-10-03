# Сделать форму для обработки добавления поста
from django import forms
from .models import PostCategory, Post, Feedback
from django.core.exceptions import ValidationError

class PostAddForm(forms.Form):
    #каждое свойство класса - это поле, которое дб в формочке
    # внутри формы можно прописать названия классов.
    title = forms.CharField(max_length=500, widget=forms.TextInput(attrs={"class": "form-control"}))
    text = forms.CharField(widget=forms.Textarea)
    category = forms.ModelChoiceField(queryset=PostCategory.objects.all())
    # title.widget.attrs.update({"class": "form-control"})

    # def clean_title(self):
    #     title = self.cleaned_data['title'] # если нужна валидация к конкретному полю, не зависимо от других
    #     if Post.objects.filter(title=title):
    #         raise ValidationError('Такой заголовок уже есть в этой категории!')
    #     return title

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        category = cleaned_data.get("category")

        if Post.objects.filter(title=title, category=category):
            raise ValidationError('Такой заголовок уже есть в этой категории!')

        return cleaned_data

    def clean_text(self): #
        text = self.cleaned_data['text'].lower()
        if 'дурак' in text:
            raise ValidationError('Нецензурное выражение')
        return text

class PostAddModelForm(forms.ModelForm):

    # title = forms.CharField(max_length=500, widget=forms.TextInput(attrs={"class": "form-control"}))
    # text = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))
    # category = forms.ModelChoiceField(queryset=PostCategory.objects.all())
    class Meta:
        model = Post
        fields = ['title', 'text', 'category']

    def __init__(self, *args, **kwargs):
        super(PostAddModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")

        if self.instance.title != title:
            category = cleaned_data.get("category")

            if Post.objects.filter(title=title, category=category):
                raise ValidationError('Такой заголовок уже есть в этой категории!')

        return cleaned_data

    def clean_text(self):
        text = self.cleaned_data['text'].lower()
        if 'дурак' in text:
            raise ValidationError('Нецензурное выражение')
        return text



class CommentAddForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(CommentAddForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    text = forms.CharField(max_length=1000, label='Текст') # label работает, только если в html не прописан

class FeedbackAddForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'text']

    def __init__(self, *args, **kwargs):
        super(FeedbackAddForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    # name = forms.CharField()
    # text = forms.CharField(widget=forms.Textarea)

    def clean_name(self):
        name = self.cleaned_data['name'].split()
        if len(name) != 2:
            raise ValidationError('Некорректный ввод имени')
        return name
