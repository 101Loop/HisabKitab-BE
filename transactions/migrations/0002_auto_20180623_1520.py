# Generated by Django 2.0.6 on 2018-06-23 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactiondetails',
            name='category',
            field=models.CharField(choices=[('C', 'Credit'), ('D', 'Debit')], max_length=8),
        ),
    ]