# Generated by Django 4.2.10 on 2024-03-21 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="students",
            name="course_id",
            field=models.ForeignKey(
                default=4,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="dashboard.courses",
            ),
        ),
    ]
