# Generated by Django 4.1.2 on 2023-01-18 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='slag',
            new_name='slug',
        ),
        migrations.RenameField(
            model_name='women',
            old_name='slag',
            new_name='slug',
        ),
    ]
