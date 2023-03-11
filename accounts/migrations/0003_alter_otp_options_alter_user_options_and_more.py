# Generated by Django 4.1.7 on 2023-03-11 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_last_logout'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='otp',
            options={'ordering': ['created_at'], 'verbose_name_plural': 'Auth OTP'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['date_joined'], 'verbose_name_plural': 'Think-In-Sphere User'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'ordering': ['created_at'], 'verbose_name_plural': 'User Profile'},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='course_name',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Current Persuing Course'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='institute_name',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Current Institute'),
        ),
    ]