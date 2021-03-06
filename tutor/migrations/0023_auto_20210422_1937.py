# Generated by Django 3.1.7 on 2021-04-22 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0022_myfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='myfile',
            name='session',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='session', to='tutor.sessions'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bill',
            name='bill_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
