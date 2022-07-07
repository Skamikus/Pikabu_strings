from django.db import models

# Create your models here.
class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    story_id = models.IntegerField(unique=True, verbose_name='id на сайте Pikabu')
    href = models.CharField(max_length=255, verbose_name='Ссылка')
    author = models.CharField(max_length=100, verbose_name='Автор')
    story_title = models.CharField(max_length=255, verbose_name='Заголовок')
    story_block = models.TextField(verbose_name='История')
    date_in = models.DateTimeField(blank=False, auto_now_add=True, verbose_name='Дата создания')
    date_change = models.DateTimeField(auto_now=True, blank=True, verbose_name='Дата изменения')
    posted = models.BooleanField(default=True, verbose_name='Публикация')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-date_in']