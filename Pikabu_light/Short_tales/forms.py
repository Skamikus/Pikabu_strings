from django import forms
from .models import Category


class PostsForm(forms.Form):
    href = forms.CharField(max_length=255, label='Ссылка на ресурс', required=False,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    author = forms.CharField(max_length=100, label='Автор', widget=forms.TextInput(attrs={"class": "form-control"}))
    story_title = forms.CharField(max_length=255, label='Заголовок поста',
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    story_block = forms.CharField(label='Текст поста', widget=forms.Textarea(attrs={"class": "form-control"}))
    posted = forms.BooleanField(label='Публикация', initial=True, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None, label='Раздел',
                                      widget=forms.Select(attrs={"class": "form-control"}))
