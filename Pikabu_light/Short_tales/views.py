from django.shortcuts import render
from django.http import HttpResponse
from .models import Posts, Category


def index(request):
    posts = Posts.objects.all()
    categories = Category.objects.all()
    context = {
        'posts': posts,
        'title': 'Все посты',
        'categories': categories,
    }
    return render(request, template_name='Short_tales/index.html', context=context)


def get_category(request, category_id):
    posts = Posts.objects.filter(category_id=category_id)
    categories = Category.objects.all()
    category = Category.objects.get(pk=category_id)
    return render(request, template_name='Short_tales/category.html',
                  context={'posts': posts, 'categories': categories, 'category': category, })


def test(request):
    return HttpResponse('<h1> Тестовая страница</h1>')
