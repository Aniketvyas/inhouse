# Generated by Django 3.0.5 on 2021-05-04 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0007_auto_20210504_1853'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lectures',
            name='LastTaughtBy',
        ),
    ]
