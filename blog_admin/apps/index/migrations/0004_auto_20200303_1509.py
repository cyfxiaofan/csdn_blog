# Generated by Django 2.2.3 on 2020-03-03 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_auto_20200227_0011'),
    ]

    operations = [
        migrations.RenameField(
            model_name='zhuanlan',
            old_name='blognumber',
            new_name='list_order',
        ),
        migrations.AddField(
            model_name='blog',
            name='ifcomment',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='blog',
            name='list_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='blogcates',
            name='list_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='zhuanlan',
            name='title',
            field=models.CharField(default='未命名', max_length=50),
        ),
        migrations.CreateModel(
            name='collect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hide', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('title', models.CharField(default='未命名', max_length=30)),
                ('desc', models.CharField(blank=True, max_length=100, null=True)),
                ('list_order', models.IntegerField(default=0)),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.Users')),
            ],
        ),
    ]
