# Generated by Django 2.0.8 on 2020-02-28 23:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date/Time')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Date/Time Modified')),
                ('advance_mode', models.BooleanField(default=False, verbose_name='Advance Mode')),
                ('is_beta', models.BooleanField(default=False, verbose_name='Is Beta User')),
                ('created_by', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Setting',
                'verbose_name_plural': 'User Settings',
            },
        ),
    ]
