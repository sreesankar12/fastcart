# Generated by Django 3.2.16 on 2023-01-17 17:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0011_auto_20230117_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referrals',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referee_referrals', to=settings.AUTH_USER_MODEL),
        ),
    ]
