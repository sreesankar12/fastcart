# Generated by Django 3.2.16 on 2022-12-21 06:09

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aboutus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('terms', ckeditor.fields.RichTextField()),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
