# Generated by Django 2.0.3 on 2018-03-09 02:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_goals'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='goals',
        ),
    ]
