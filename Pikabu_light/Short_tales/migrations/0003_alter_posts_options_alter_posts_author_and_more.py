# Generated by Django 4.0.5 on 2022-07-07 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Short_tales', '0002_alter_posts_posted'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='posts',
            options={'ordering': ['-date_in'], 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
        migrations.AlterField(
            model_name='posts',
            name='author',
            field=models.CharField(max_length=100, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='date_change',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата изменения'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='date_in',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='href',
            field=models.CharField(max_length=255, verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='posts',
            name='posted',
            field=models.BooleanField(default=True, verbose_name='Публикация'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='story_block',
            field=models.TextField(verbose_name='История'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='story_id',
            field=models.IntegerField(unique=True, verbose_name='id на сайте Pikabu'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='story_title',
            field=models.CharField(max_length=255, verbose_name='Заголовок'),
        ),
    ]
