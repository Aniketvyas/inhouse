# Generated by Django 3.2 on 2021-06-18 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0026_auto_20210618_2024'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weightage',
            old_name='subjects',
            new_name='subject',
        ),
    ]
