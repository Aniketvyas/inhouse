# Generated by Django 3.2 on 2021-06-16 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0024_auto_20210616_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizgrades',
            name='startedOn',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='quizgrades',
            name='timeTaken',
            field=models.DurationField(blank=True, null=True),
        ),
    ]