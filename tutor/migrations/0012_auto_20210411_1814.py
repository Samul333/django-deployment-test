# Generated by Django 3.1.7 on 2021-04-11 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0011_auto_20210411_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]
