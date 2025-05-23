# Generated by Django 5.1.5 on 2025-01-17 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0013_quote"),
        ("users", "0003_student_completed_challenge_questions_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="correct_challenge_questions",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="correct_challenge_questions",
                to="main.question",
            ),
        ),
        migrations.AddField(
            model_name="student",
            name="correct_quiz_questions",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="correct_quiz_questions",
                to="main.quizquestion",
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="completed_challenge_questions",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="completed_challenge_questions",
                to="main.question",
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="completed_quiz_questions",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="completed_quiz_questions",
                to="main.quizquestion",
            ),
        ),
    ]
