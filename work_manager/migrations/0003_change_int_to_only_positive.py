# Generated by Django 3.1.7 on 2023-05-26 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_manager', '0002_revise_spelling'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='room',
            field=models.PositiveIntegerField(),
        ),
    ]