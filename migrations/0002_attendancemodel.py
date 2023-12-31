# Generated by Django 4.2.4 on 2023-08-24 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('more', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkin', models.DateTimeField(blank=True, null=True)),
                ('checkin_image', models.ImageField(blank=True, default='', null=True, upload_to='checkin/')),
                ('lat', models.CharField(blank=True, default=0.0, max_length=100, null=True)),
                ('long', models.CharField(blank=True, default=0.0, max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='more.userlogin')),
            ],
        ),
    ]
