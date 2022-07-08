from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, CreateView

from .models import Posts, Category
from .forms import PostsForm


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
