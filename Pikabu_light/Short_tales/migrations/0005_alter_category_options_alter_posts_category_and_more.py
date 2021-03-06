# Generated by Django 4.0.5 on 2022-07-07 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Short_tales', '0004_category_posts_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterField(
            model_name='posts',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Short_tales.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='href',
            field=models.CharField(blank=True, max_length=255, verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='story_id',
            field=models.IntegerField(blank=True, unique=True, verbose_name='id на сайте Pikabu'),
        ),
    ]
