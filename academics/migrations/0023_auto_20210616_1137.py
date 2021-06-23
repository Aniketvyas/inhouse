# Generated by Django 3.2 on 2021-06-16 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0022_alter_assignmentsubmission_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizgrades',
            name='correctAnswers',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='quizgrades',
            name='unAttemptedQuestions',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='quizgrades',
            name='wrongAnswers',
            field=models.IntegerField(null=True),
        ),
    ]