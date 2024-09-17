from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):

    username = forms.CharField(max_length=500)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs): # добавили request
        self.request = request
        self.user = None #при инициализации объектра пользователь не авторизован
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def get_user(self): # встроенная функция
        return self.user

    def clean(self):
        #достать данные
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        self.user = authenticate(self.request, username=username, password=password)
        if not self.user:
            raise ValidationError('Неверный логин или пароль')
