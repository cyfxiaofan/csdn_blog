# Generated by Django 2.2.3 on 2020-04-15 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_auto_20200415_1658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='sex',
        ),
    ]