# Generated by Django 3.2 on 2021-05-30 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0017_assignment_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='startingDate',
            field=models.DateField(null=True),
        ),
    ]
