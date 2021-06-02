# Generated by Django 3.1.7 on 2021-06-02 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_auto_20210601_1809'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='collection',
            constraint=models.UniqueConstraint(fields=('url_name', 'company'), name='unique_url_name_company'),
        ),
    ]
