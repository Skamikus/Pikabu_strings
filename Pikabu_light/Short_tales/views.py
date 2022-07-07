from django.shortcuts import render
from django.http import HttpResponse
from .models import Posts, Category


def index(request):
    posts = Posts.objects.all()
    context = {
        'posts': posts,
        'title': 'Все посты',
    }
    return render(request, template_name='Short_tales/index.html', context=context)


def get_category(request, category_id):
    posts = Posts.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, template_name='Short_tales/category.html',
                  context={'posts': posts, 'category': category, })


def test(request):
    return HttpResponse('<h1> Тестовая страница</h1>')
