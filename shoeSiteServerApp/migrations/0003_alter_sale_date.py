# Generated by Django 4.0.5 on 2022-06-16 04:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoeSiteServerApp', '0002_shoe_thumbnail_alter_sale_date_alter_shoe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 16, 4, 57, 6, 727885)),
        ),
    ]
