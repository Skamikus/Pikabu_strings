from django import forms
from .models import Posts


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