# Generated by Django 4.0.5 on 2022-06-16 06:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoeSiteServerApp', '0003_alter_sale_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 16, 6, 42, 12, 416768)),
        ),
    ]