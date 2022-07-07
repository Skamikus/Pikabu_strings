from django.shortcuts import render
from django.http import HttpResponse
from .models import Posts

def index(request):
    posts = Posts.objects.all()
    context = {
        'posts': posts,
        'title': 'Список постов',
    }
    return render(request, template_name='Short_tales/index.html', context=context)

def test(request):
    return HttpResponse('<h1> Тестовая страница</h1>')