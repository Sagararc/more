# Generated by Django 4.2.3 on 2023-08-30 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('more', '0007_remove_attendancemodel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancemodel',
            name='user',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]