# Generated by Django 2.1 on 2018-11-19 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_auto_20181119_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventdata',
            name='Contact_Us',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]