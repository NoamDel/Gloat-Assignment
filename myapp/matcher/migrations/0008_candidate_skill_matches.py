# Generated by Django 3.2.13 on 2022-05-31 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matcher', '0007_alter_job_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='skill_matches',
            field=models.IntegerField(default=0),
        ),
    ]
