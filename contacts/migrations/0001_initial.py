# Generated by Django 2.0.6 on 2018-06-20 10:32

from django.db import migrations, models
import django_custom_modules.db_type


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified', django_custom_modules.db_type.UnixTimestampField(auto_created=True)),
                ('create_date', django_custom_modules.db_type.UnixTimestampField(auto_now_add=True)),
                ('name', models.CharField(max_length=254, verbose_name='Unique UserName')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='Email Address')),
                ('mobile', models.CharField(max_length=15, null=True, verbose_name='Mobile Number')),
            ],
        ),
    ]
