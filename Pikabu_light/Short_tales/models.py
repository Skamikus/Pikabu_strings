from django.db import models
from django.urls import reverse

# Create your models here.
class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    story_id = models.IntegerField(unique=True, verbose_name='id на сайте Pikabu', blank=True, null=True,)
    href = models.CharField(max_length=255, verbose_name='Ссылка', blank=True)
    author = models.CharField(max_length=100, verbose_name='Автор')
    story_title = models.CharField(max_length=255, verbose_name='Заголовок')
    story_block = models.TextField(verbose_name='История')
    date_in = models.DateTimeField(blank=False, auto_now_add=True, verbose_name='Дата создания')
    date_change = models.DateTimeField(auto_now=True, blank=True, verbose_name='Дата изменения')
    posted = models.BooleanField(default=True, verbose_name='Публикация')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True, default='1', verbose_name='Категория')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-date_in']


class Category(models.Model):
    title = models.CharField(max_length=50, db_index=True, verbose_name='Категория')

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    def __str__(self):
        return self.title