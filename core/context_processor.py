from django.conf import settings

def add_host(request):
    return {'HOST': settings.HOST}