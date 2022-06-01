# Generated by Django 3.2.13 on 2022-06-01 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matcher', '0008_candidate_skill_matches'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='experience',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='candidate',
            name='name_match',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='job',
            name='max_candidates',
            field=models.IntegerField(default=1),
        ),
    ]