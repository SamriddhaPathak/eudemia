# Generated by Django 5.1.5 on 2025-01-20 16:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0023_alter_challengetracker_current_question"),
        ("users", "0007_alter_student_blood_group_alter_student_level"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShopItem",
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
                ("name", models.CharField(max_length=50)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="reward_images"),
                ),
                ("cost", models.PositiveIntegerField()),
                ("item_type", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="ShopItemPurchase",
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
                ("purchased_at", models.DateTimeField(auto_now_add=True)),
                (
                    "shop_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="purchases",
                        to="main.shopitem",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="purchases",
                        to="users.student",
                    ),
                ),
            ],
        ),
    ]
