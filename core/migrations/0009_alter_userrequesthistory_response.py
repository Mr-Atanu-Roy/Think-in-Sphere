# Generated by Django 4.1.7 on 2023-03-07 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_userrequesthistory_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrequesthistory',
            name='response',
            field=models.TextField(blank=True, null=True),
        ),
    ]
