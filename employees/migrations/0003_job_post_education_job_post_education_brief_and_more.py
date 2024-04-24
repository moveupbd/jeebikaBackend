# Generated by Django 5.0.3 on 2024-04-24 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_remove_employee_license_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job_post',
            name='education',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job_post',
            name='education_brief',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job_post',
            name='source',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='job_post',
            name='source_prove',
            field=models.FileField(blank=True, null=True, upload_to='sources/'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='license_copy',
            field=models.FileField(blank=True, null=True, upload_to='license_copies/'),
        ),
    ]
