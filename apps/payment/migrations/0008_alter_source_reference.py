# Generated by Django 3.2.16 on 2023-01-19 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_alter_source_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='reference',
            field=models.CharField(blank=True, max_length=1000, verbose_name='Reference'),
        ),
    ]
