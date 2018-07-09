# Generated by Django 2.0.6 on 2018-07-09 18:48

from django.db import migrations, models
import django_custom_modules.db_type


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=200, verbose_name='message')),
                ('name', models.CharField(max_length=254, verbose_name='Unique UserName')),
                ('email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('mobile', models.CharField(max_length=15, null=True, verbose_name='Mobile Number')),
                ('create_date', django_custom_modules.db_type.UnixTimestampField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Feedback',
                'verbose_name_plural': 'Feedbacks',
            },
        ),
    ]
