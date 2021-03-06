# Generated by Django 3.1.2 on 2021-01-08 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210108_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.EmailField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. email form only.', max_length=254, unique=True),
        ),
    ]
