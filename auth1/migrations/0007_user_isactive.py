# Generated by Django 4.2.16 on 2024-09-29 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth1', '0006_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
    ]
