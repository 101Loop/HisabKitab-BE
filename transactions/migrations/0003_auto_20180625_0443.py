# Generated by Django 2.0.6 on 2018-06-25 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20180623_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactiondetails',
            name='amount',
            field=models.IntegerField(),
        ),
    ]
