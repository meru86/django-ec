# Generated by Django 3.1.7 on 2021-03-18 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_post_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
