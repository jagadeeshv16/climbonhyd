# Generated by Django 2.1 on 2018-11-19 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_auto_20181119_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventdata',
            name='active',
            field=models.BooleanField(default=False, verbose_name='active'),
        ),
    ]
