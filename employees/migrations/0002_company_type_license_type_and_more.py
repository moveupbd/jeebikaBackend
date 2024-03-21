# Generated by Django 4.2.1 on 2024-03-21 07:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='company_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='License_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='registration_number',
            new_name='license_number',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='id_pic_back',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='id_pic_front',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='trade_number',
        ),
        migrations.AddField(
            model_name='employee',
            name='company_logo',
            field=models.ImageField(blank=True, null=True, upload_to='images/company_logos/'),
        ),
        migrations.AddField(
            model_name='employee',
            name='company_owner',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='employee_address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='employee_designation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='employee_email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='employee_mobile',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='id_card_back',
            field=models.ImageField(blank=True, null=True, upload_to='images/id_pics_back/'),
        ),
        migrations.AddField(
            model_name='employee',
            name='id_card_front',
            field=models.ImageField(blank=True, null=True, upload_to='images/id_pics_front/'),
        ),
        migrations.AddField(
            model_name='employee',
            name='license_copy',
            field=models.ImageField(blank=True, null=True, upload_to='images/license_copies/'),
        ),
        migrations.AddField(
            model_name='job_post',
            name='department',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='job_post',
            name='job_desc',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job_post',
            name='other_facilities',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job_post',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='job_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='job_post',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.category'),
        ),
        migrations.AlterField(
            model_name='job_post',
            name='compensation',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='job_post',
            name='service_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.service_type'),
        ),
        migrations.AddField(
            model_name='employee',
            name='license_type',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='employees.license_type'),
        ),
        migrations.AddField(
            model_name='job_post',
            name='company_type',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='employees.company_type'),
        ),
    ]