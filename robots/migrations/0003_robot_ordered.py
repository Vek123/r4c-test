# Generated by Django 5.1.4 on 2024-12-16 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("robots", "0002_alter_robot_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="robot",
            name="ordered",
            field=models.BooleanField(blank=True, db_default=False),
        ),
    ]
