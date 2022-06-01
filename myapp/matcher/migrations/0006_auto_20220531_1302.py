# Generated by Django 3.2.13 on 2022-05-31 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matcher', '0005_auto_20220531_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='skills',
            field=models.ManyToManyField(related_name='candidates', to='matcher.Skill'),
        ),
        migrations.AlterField(
            model_name='job',
            name='skills',
            field=models.ManyToManyField(related_name='jobs', to='matcher.Skill'),
        ),
    ]
