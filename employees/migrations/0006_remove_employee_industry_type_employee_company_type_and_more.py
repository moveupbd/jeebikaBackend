# Generated by Django 5.0.3 on 2024-04-01 07:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0005_remove_job_post_company_title_job_post_company_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='industry_type',
        ),
        migrations.AddField(
            model_name='employee',
            name='company_type',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='employees.company_type'),
        ),
        migrations.DeleteModel(
            name='Industry_type',
        ),
    ]
