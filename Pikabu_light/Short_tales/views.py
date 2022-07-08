from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Posts, Category
from .forms import PostsForm

def index(request):
    posts = Posts.objects.all()
    context = {
        'posts': posts,
        'title': 'Все посты',
    }
    return render(request, template_name='Short_tales/index.html', context=context)


def get_category(request, category_id):
    posts = Posts.objects.filter(category_id=category_id)
    # category = Category.objects.get(pk=category_id)
    category = get_object_or_404(Category, pk=category_id)
    return render(request, template_name='Short_tales/category.html',
                  context={'posts': posts, 'category': category, })


def add_post(request):
    if request.method == 'POST':
        form = PostsForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            # Posts.objects.create(**form.cleaned_data)
            form.save()
            return redirect('home')
    else:
        form = PostsForm()
    return render(request, 'Short_tales/add_post.html', {'form': form})

def test(request):
    return HttpResponse('<h1> Тестовая страница</h1>')
