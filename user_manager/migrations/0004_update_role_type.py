# Generated by Django 3.1.7 on 2023-05-26 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0003_rename_User_to_Guest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role_type',
            field=models.IntegerField(choices=[(0, 'Guest'), (1, 'Maid'), (2, 'Supervisor')], default=0),
        ),
    ]
