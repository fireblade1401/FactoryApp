# Generated by Django 4.2.6 on 2023-10-13 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_telegram_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='telegram_token',
            field=models.CharField(blank=True, default='<function uuid4 at 0x7fde198af640>', max_length=100, null=True),
        ),
    ]
