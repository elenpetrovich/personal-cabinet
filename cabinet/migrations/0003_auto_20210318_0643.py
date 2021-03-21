# Generated by Django 3.1.7 on 2021-03-18 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0002_auto_20210318_0637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='companies',
        ),
        migrations.AddField(
            model_name='role',
            name='company',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='cabinet.company'),
        ),
    ]
