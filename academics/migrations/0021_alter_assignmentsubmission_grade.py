# Generated by Django 3.2 on 2021-06-16 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0020_assignmentsubmission_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='grade',
            field=models.IntegerField(blank=True),
        ),
    ]
