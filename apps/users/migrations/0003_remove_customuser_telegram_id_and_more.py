# Generated by Django 4.2.6 on 2023-10-12 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_telegram_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='telegram_id',
        ),
        migrations.AddField(
            model_name='customuser',
            name='telegram_chat_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='telegram_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
