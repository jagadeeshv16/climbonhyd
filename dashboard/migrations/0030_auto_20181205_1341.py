# Generated by Django 2.1 on 2018-12-05 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0029_auto_20181205_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photos',
            name='thumbnail_url',
            field=models.URLField(max_length=1000),
        ),
    ]
