# Generated by Django 4.1.2 on 2022-11-26 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='domaine',
        ),
    ]
