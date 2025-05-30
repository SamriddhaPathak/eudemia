from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0012_quiz_quizquestion_quiz"),
    ]

    operations = [
        migrations.CreateModel(
            name="Quote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quote", models.TextField(max_length=1000)),
                ("by", models.TextField(max_length=50)),
            ],
        ),
    ]
