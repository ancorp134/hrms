# Generated by Django 4.2.7 on 2023-12-16 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_holiday'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='email',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='last_name',
        ),
    ]