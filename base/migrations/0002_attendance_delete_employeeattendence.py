# Generated by Django 4.2.7 on 2023-12-25 07:13

import base.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.CharField(default=base.models.generate_unique_id, editable=False, max_length=25, primary_key=True, serialize=False)),
                ('in_Time', models.TimeField(blank=True, null=True)),
                ('in_Date', models.DateField(blank=True, null=True)),
                ('out_Time', models.TimeField(blank=True, null=True)),
                ('out_Date', models.DateField(blank=True, null=True)),
                ('in_Location', models.CharField(blank=True, max_length=200, null=True)),
                ('out_Location', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(blank=True, max_length=20, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.employee')),
            ],
        ),
        migrations.DeleteModel(
            name='EmployeeAttendence',
        ),
    ]
