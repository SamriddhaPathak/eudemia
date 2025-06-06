# Generated by Django 5.1.5 on 2025-01-19 14:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0019_challengetracker_completed_at"),
        ("users", "0006_alter_userprofile_profile_pic"),
    ]

    operations = [
        migrations.AddField(
            model_name="challenge",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="users.teacher",
            ),
        ),
    ]
