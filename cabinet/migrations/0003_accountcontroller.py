# Generated by Django 3.1.7 on 2021-06-01 18:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_auto_20210601_1808'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cabinet', '0002_registrationrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountController',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accounts', to='company.company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='controller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]