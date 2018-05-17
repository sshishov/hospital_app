# Generated by Django 2.0.4 on 2018-06-06 18:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields
import hospital.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Added')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('values', djongo.models.fields.ArrayModelField(model_container=hospital.models.ParameterValue, verbose_name='Values')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Application',
                'verbose_name_plural': 'Applications',
            },
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Added')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('code', models.CharField(max_length=10, verbose_name='Code')),
            ],
            options={
                'verbose_name': 'Form',
                'verbose_name_plural': 'Forms',
            },
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Added')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('field_type', models.IntegerField(choices=[(1, 'Integer'), (3, 'String'), (2, 'Float'), (4, 'Multistring'), (5, 'Boolean'), (6, 'Date'), (7, 'Datetime')], verbose_name='Type')),
            ],
            options={
                'verbose_name': 'Parameter',
                'verbose_name_plural': 'Parameters',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Added')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('full_name', models.CharField(max_length=100, verbose_name='Full Name')),
                ('birthday', models.DateField(verbose_name='Birthday')),
            ],
            options={
                'verbose_name': 'Patient',
                'verbose_name_plural': 'Patients',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Added')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('code', models.CharField(max_length=10, verbose_name='Code')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('subject', models.CharField(max_length=100, verbose_name='Subject')),
                ('district', models.CharField(max_length=100, verbose_name='District')),
                ('projects', models.ManyToManyField(to='hospital.Project', verbose_name='Projects')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.AddField(
            model_name='form',
            name='fields',
            field=models.ManyToManyField(to='hospital.Parameter', verbose_name='Fields'),
        ),
        migrations.AddField(
            model_name='form',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.Project', verbose_name='Project'),
        ),
        migrations.AddField(
            model_name='application',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Doctor'),
        ),
        migrations.AddField(
            model_name='application',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.Form', verbose_name='Form'),
        ),
        migrations.AddField(
            model_name='application',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.Application', verbose_name='Parent'),
        ),
        migrations.AddField(
            model_name='application',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.Patient', verbose_name='Patient'),
        ),
    ]
