# Generated by Django 3.2.13 on 2022-06-01 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matcher', '0009_auto_20220601_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
