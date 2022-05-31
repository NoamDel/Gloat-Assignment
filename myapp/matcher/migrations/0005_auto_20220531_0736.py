# Generated by Django 3.2.13 on 2022-05-31 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matcher', '0004_auto_20220530_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='candidate',
        ),
        migrations.RemoveField(
            model_name='skill',
            name='job',
        ),
        migrations.AddField(
            model_name='candidate',
            name='skills',
            field=models.ManyToManyField(to='matcher.Skill'),
        ),
        migrations.AddField(
            model_name='job',
            name='skills',
            field=models.ManyToManyField(to='matcher.Skill'),
        ),
    ]
