# Generated by Django 3.2.13 on 2022-05-30 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matcher', '0003_auto_20220530_1352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='job',
        ),
        migrations.AddField(
            model_name='skill',
            name='job',
            field=models.ManyToManyField(to='matcher.Job'),
        ),
    ]
