# Generated by Django 2.1 on 2018-11-21 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_eventdata_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('highres_link', models.URLField()),
                ('thumb_link', models.URLField()),
                ('photo_id', models.CharField(max_length=255)),
                ('photo_link', models.CharField(max_length=55)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.EventData')),
            ],
        ),
    ]
