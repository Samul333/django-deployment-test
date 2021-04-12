# Generated by Django 3.1.7 on 2021-04-08 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0005_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subjects', to=settings.AUTH_USER_MODEL),
        ),
    ]
