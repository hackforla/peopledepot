# Generated by Django 4.0.10 on 2023-05-19 00:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('url', models.URLField(blank=True)),
                ('logo', models.URLField(blank=True)),
                ('active', models.BooleanField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
