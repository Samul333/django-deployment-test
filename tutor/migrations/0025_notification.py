# Generated by Django 3.2 on 2021-04-22 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0024_myfile_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recepient', models.CharField(max_length=30)),
                ('notification', models.BooleanField(default=False)),
                ('date_at', models.DateTimeField(auto_now_add=True)),
                ('seession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutor.sessions')),
            ],
        ),
    ]
