# Generated by Django 4.1 on 2022-08-30 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telephone',
            field=models.CharField(max_length=11, unique=True, verbose_name='手机号'),
        ),
    ]