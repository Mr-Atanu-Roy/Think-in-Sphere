# Generated by Django 4.1.7 on 2023-03-03 10:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatroom',
            options={'verbose_name_plural': 'Chat Rooms'},
        ),
        migrations.AlterModelOptions(
            name='userrequesthistory',
            options={'verbose_name_plural': 'User Search History'},
        ),
        migrations.AddField(
            model_name='chatroom',
            name='room_name',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='room_id',
            field=models.UUIDField(default=uuid.UUID('d3d3d8e6-1008-45df-b293-f07cb84be2c4')),
        ),
    ]