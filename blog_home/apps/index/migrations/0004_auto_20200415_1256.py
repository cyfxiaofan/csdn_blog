# Generated by Django 2.2.3 on 2020-04-15 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_comment_affim_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='affirm_blog',
            field=models.TextField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='bghistory',
            field=models.TextField(blank=True, default=0, null=True),
        ),
    ]
