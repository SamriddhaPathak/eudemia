# Generated by Django 5.1.5 on 2025-01-19 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0021_alter_question_question_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="unit",
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
