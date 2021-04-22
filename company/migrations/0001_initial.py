# Generated by Django 3.1.7 on 2021-04-22 18:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_name', models.CharField(max_length=254, verbose_name='Название')),
                ('link_name', models.CharField(max_length=254, verbose_name='Ссылка')),
                ('schema', models.JSONField(verbose_name='Схема')),
                ('mongo_collection', models.CharField(max_length=254, verbose_name='MongoDB')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_name', models.SlugField(max_length=254, unique=True, verbose_name='Уникальное название')),
                ('short_name', models.CharField(max_length=254, verbose_name='Короткое название')),
                ('full_name', models.CharField(max_length=510, verbose_name='Полное название')),
                ('city', models.CharField(max_length=254, verbose_name='Город')),
                ('address', models.CharField(max_length=254, verbose_name='Адрес')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта')),
                ('mongo_db', models.CharField(max_length=254, verbose_name='MongoDB')),
                ('is_public', models.BooleanField(default=False, verbose_name='Публичность')),
                ('secret_key', models.SlugField(max_length=254, verbose_name='Ключ доступа')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, verbose_name='Название')),
                ('collections', models.ManyToManyField(related_name='roles', to='company.Collection')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='company.company')),
                ('users', models.ManyToManyField(related_name='roles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='collection',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collections', to='company.company'),
        ),
    ]
