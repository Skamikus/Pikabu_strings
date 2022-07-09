from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, CreateView
from django.contrib import messages
from django.contrib.auth import login, logout

from .models import Posts, Category
from .forms import PostsForm, UserRegisterForm, UserLoginForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            lofin(request, user)
            messages.success(request, 'Регистрация прошла успешно')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'Short_tales/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ошибка аутентификации')
    else:
        form = UserLoginForm()
    return render(request, 'Short_tales/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

class HomePosts(ListView):
    model = Posts
    template_name = 'Short_tales/index.html'
    context_object_name = 'posts'
    paginate_by = 10
    # extra_context = {'title': 'Главная'}


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context

    def get_queryset(self):
        return Posts.objects.filter(posted=True)


class CategoryPosts(ListView):
    model = Posts
    template_name = 'Short_tales/category.html'
    context_object_name = 'posts'
    paginate_by = 10
    # extra_context = {'title': 'Главная'}
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return Posts.objects.filter(category=self.kwargs['category_id'], posted=True)


class AddPosts(CreateView):
    form_class = PostsForm
    template_name = 'Short_tales/add_post.html'


def test(request):
    return HttpResponse('<h1> Тестовая страница</h1>')
