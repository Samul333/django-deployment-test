# Generated by Django 3.2 on 2021-04-16 18:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0016_sessions_is_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessions',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tutor', to=settings.AUTH_USER_MODEL),
        ),
    ]
