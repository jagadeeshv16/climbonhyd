# Generated by Django 2.1 on 2018-11-14 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20181114_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='photos',
            field=models.ImageField(blank=True, upload_to='media/photos/'),
        ),
    ]
