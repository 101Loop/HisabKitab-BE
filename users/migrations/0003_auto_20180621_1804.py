# Generated by Django 2.0.6 on 2018-06-21 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180620_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpvalidation',
            name='type',
            field=models.CharField(choices=[('mobile', 'Mobile Number'), ('email', 'EMail Address')], default='email', max_length=15, verbose_name='EMail/Mobile'),
        ),
    ]
