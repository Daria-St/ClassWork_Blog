import requests

# for i in range(3):
#     r = requests.get("http://127.0.0.1:8000/")
#     print(r.text)

# добавили во вьюху from django.views.decorators.csrf import csrf_exempt и декоратор @csrf_exempt на post_detail и убираем токен {% csrf_token %} в post_detail.html
for i in range(3):
    r = requests.post("http://127.0.0.1:8000/posts/2", data={"text": 'Пам'})
    print(r)