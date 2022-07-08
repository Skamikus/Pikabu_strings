from django import forms
from .models import Posts
import re
from django.core.exceptions import ValidationError


class PostsForm(forms.ModelForm):
    class Meta:
        model = Posts
        # fields = '__all__'
        fields = ['href', 'author', 'story_title', 'story_block', 'posted', 'category']
        widgets = {
            'href': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'story_title': forms.TextInput(attrs={'class': 'form-control'}),
            'story_block': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}, choices='Свежее'),
        }

    def clean_author(self):
        author = self.cleaned_data['author']
        if re.match(r'\d', author):
            raise ValidationError('Имя не должно начинаться с цифры')
        return author
