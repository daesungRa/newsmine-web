# Generated by Django 3.1.2 on 2021-01-19 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210108_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='thumbnail_image',
            field=models.ImageField(blank=True, upload_to='profile_images'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to='profile_images'),
        ),
    ]