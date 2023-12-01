# Generated by Django 4.2.7 on 2023-12-01 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='slug',
        ),
        migrations.AddField(
            model_name='department',
            name='department_code',
            field=models.CharField(blank=True, max_length=5, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='department',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]