# Generated by Django 2.0.6 on 2018-06-29 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='mobile',
            field=models.CharField(max_length=15, null=True, verbose_name='Mobile Number'),
        ),
    ]
