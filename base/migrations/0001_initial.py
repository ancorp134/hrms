# Generated by Django 4.2.7 on 2023-11-23 12:13

import base.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.CharField(default=base.models.generate_unique_id, editable=False, max_length=25, primary_key=True, serialize=False)),
                ('branch_name', models.CharField(max_length=100, unique=True)),
                ('slug', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.CharField(default=base.models.generate_unique_id, editable=False, max_length=25, primary_key=True, serialize=False)),
                ('department', models.CharField(max_length=100, unique=True)),
                ('slug', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.CharField(default=base.models.generate_unique_id, editable=False, max_length=25, primary_key=True, serialize=False)),
                ('designation', models.CharField(max_length=100, unique=True)),
                ('slug', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.CharField(default=base.models.generate_unique_id, editable=False, max_length=25, primary_key=True, serialize=False)),
                ('employee_code', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('official_email', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('punching_code', models.IntegerField(blank=True, null=True, unique=True)),
                ('date_of_joining', models.DateField(null=True)),
                ('employee_type', models.CharField(choices=[('Permanent', 'Permanent')], max_length=100)),
                ('shift', models.CharField(choices=[('General', 'General'), ('UNICEF', 'UNICEF')], max_length=100)),
                ('grade', models.CharField(choices=[('Employee', 'Employee'), ('Consultant', 'Consultant'), ('UNF Employee', 'UNF Employee'), ('UNF Supervisor', 'UNF Supervisor')], max_length=100)),
                ('ctc', models.CharField(blank=True, max_length=20, null=True)),
                ('gross_salary', models.CharField(blank=True, max_length=20, null=True)),
                ('basic_salary', models.CharField(blank=True, max_length=20, null=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.branch')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.department')),
                ('designation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.designation')),
                ('reporting_manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reportees', to='base.employee')),
                ('user', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RequiredDocument',
            fields=[
                ('id', models.CharField(default=base.models.generate_unique_id, editable=False, max_length=25, primary_key=True, serialize=False)),
                ('document_type', models.CharField(blank=True, choices=[('Aadhar Card', 'Aadhar Card'), ('Cancelled Cheque/Bank Passbook', 'Cancelled Cheque/Bank Passbook'), ('CV/Resume', 'CV/Resume'), ('Educational Certificates', 'Educational Certificates'), ('Experience/Employment Documents', 'Experience/Employment Documents'), ('Inductus Offer/Appointment Letter', 'Inductus Offer/Appointment Letter'), ('Other/All Documents', 'Other/All Documents'), ('PAN Card', 'PAN Card'), ('Salary Proof-Salary Slip/Bank Statement', 'Salary Proof-Salary Slip/Bank Statement')], max_length=100, null=True)),
                ('document', models.FileField(upload_to=base.models.get_upload_path)),
                ('comments', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_expiry', models.DateField(blank=True, null=True)),
                ('employee', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='base.employee')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalInformation',
            fields=[
                ('id', models.CharField(default=base.models.generate_unique_id, editable=False, max_length=25, primary_key=True, serialize=False)),
                ('father_name', models.CharField(blank=True, max_length=100, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile_no', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('blood_group', models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=10, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('tehsil', models.CharField(blank=True, max_length=100, null=True)),
                ('district', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, choices=[('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'), ('Andhra Pradesh', 'Andhra Pradesh'), ('Arunachal Pradesh', 'Arunachal Pradesh'), ('Assam', 'Assam'), ('Bihar', 'Bihar'), ('Chandigarh', 'Chandigarh'), ('Chhattisgarh', 'Chhattisgarh'), ('Dadra and Nagar Haveli', 'Dadra and Nagar Haveli'), ('Daman and Diu', 'Daman and Diu'), ('Delhi', 'Delhi'), ('Goa', 'Goa'), ('Gujarat', 'Gujarat'), ('Haryana', 'Haryana'), ('Himachal Pradesh', 'Himachal Pradesh'), ('Jammu and Kashmir', 'Jammu and Kashmir'), ('Jharkhand', 'Jharkhand'), ('Karnataka', 'Karnataka'), ('Kerala', 'Kerala'), ('Lakshadweep', 'Lakshadweep'), ('Madhya Pradesh', 'Madhya Pradesh'), ('Maharashtra', 'Maharashtra'), ('Manipur', 'Manipur'), ('Meghalaya', 'Meghalaya'), ('Mizoram', 'Mizoram'), ('Nagaland', 'Nagaland'), ('Odisha', 'Odisha'), ('Puducherry', 'Puducherry'), ('Punjab', 'Punjab'), ('Rajasthan', 'Rajasthan'), ('Sikkim', 'Sikkim'), ('Tamil Nadu', 'Tamil Nadu'), ('Telangana', 'Telangana'), ('Tripura', 'Tripura'), ('Uttar Pradesh', 'Uttar Pradesh'), ('Uttarakhand', 'Uttarakhand'), ('West Bengal', 'West Bengal')], max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('pincode', models.CharField(blank=True, max_length=10, null=True)),
                ('nationality', models.CharField(blank=True, max_length=10, null=True)),
                ('cast_category', models.CharField(blank=True, max_length=20, null=True)),
                ('employee', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='base.employee')),
            ],
        ),
    ]
