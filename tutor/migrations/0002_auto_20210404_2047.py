# Generated by Django 3.1.7 on 2021-04-04 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='student_emailaddress',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='student_username',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='user',
            name='student_password',
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=30),
        ),
    ]
