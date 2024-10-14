# Generated by Django 5.1.1 on 2024-09-27 19:05

import base.models
import django.db.models.deletion
import shortuuidfield.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='requestTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, unique=True)),
                ('refund_type', models.CharField(max_length=15)),
                ('request_status', models.CharField(choices=[('in_review', 'In Review'), ('accepted', 'Accepted'), ('checked', 'Checked'), ('refunded', 'Refunded'), ('rejected', 'Rejected')], max_length=15)),
                ('uid', models.CharField(default='random', max_length=100)),
                ('raised_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='requestRemarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, unique=True)),
                ('remarks_salesman', models.CharField(max_length=250)),
                ('remarks_receiver', models.CharField(max_length=250)),
                ('remarks_checker', models.CharField(max_length=250)),
                ('request_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.requesttable')),
            ],
        ),
        migrations.CreateModel(
            name='requestImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, unique=True)),
                ('image_salesman', models.ImageField(default='product.jpg', upload_to=base.models.user_directory_path)),
                ('image_checker_1', models.ImageField(default='product.jpg', upload_to=base.models.user_directory_path)),
                ('image_checker_2', models.ImageField(default='product.jpg', upload_to=base.models.user_directory_path)),
                ('request_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.requesttable')),
            ],
        ),
        migrations.CreateModel(
            name='rejectedRequestTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rejid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, unique=True)),
                ('rejected_by', models.CharField(max_length=250)),
                ('rejection_reason', models.CharField(max_length=250)),
                ('rid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.requesttable')),
            ],
        ),
        migrations.CreateModel(
            name='inoviceTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, unique=True)),
                ('invoice', models.ImageField(default='product.jpg', upload_to=base.models.user_directory_path)),
                ('rid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.requesttable')),
            ],
        ),
        migrations.CreateModel(
            name='urgentRequestTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, unique=True)),
                ('urgency_reason', models.CharField(max_length=250)),
                ('urgency_status', models.CharField(choices=[('in_review', 'In Review'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], max_length=15)),
                ('denial_reason', models.CharField(max_length=250)),
                ('rid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.requesttable')),
            ],
        ),
        migrations.CreateModel(
            name='vendorTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, unique=True)),
                ('proprietor_name', models.CharField(default='Proprietor Name', max_length=100)),
                ('company_name', models.CharField(default='Company Name', max_length=100)),
                ('address', models.CharField(default='Address', max_length=200)),
                ('phone_number', models.PositiveIntegerField()),
                ('total_requests', models.PositiveIntegerField(null=True)),
                ('salesman_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='requesttable',
            name='vid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.vendortable'),
        ),
    ]
