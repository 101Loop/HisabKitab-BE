# Generated by Django 2.2.10 on 2020-02-29 09:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200229_0241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpvalidation',
            name='reactive_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='ReActivate Sending OTP'),
        ),
    ]