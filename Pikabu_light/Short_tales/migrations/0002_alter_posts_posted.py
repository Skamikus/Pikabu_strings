# Generated by Django 4.0.5 on 2022-07-07 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Short_tales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='posted',
            field=models.BooleanField(default=True),
        ),
    ]