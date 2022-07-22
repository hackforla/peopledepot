# Generated by Django 4.0.4 on 2022-06-23 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_user_phone_remove_user_time_zone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_status',
            field=models.CharField(choices=[('ac', 'Active'), ('in', 'Inactive'), ('re', 'Removed')], default='ac', max_length=2),
        ),
    ]