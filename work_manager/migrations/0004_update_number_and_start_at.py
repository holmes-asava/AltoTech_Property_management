# Generated by Django 3.1.7 on 2023-05-26 19:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('work_manager', '0003_change_int_to_only_positive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='start_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='work_order_number',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
