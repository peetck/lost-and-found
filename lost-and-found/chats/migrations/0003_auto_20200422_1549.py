# Generated by Django 3.0.3 on 2020-04-22 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_auto_20200411_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]