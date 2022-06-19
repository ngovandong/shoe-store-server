# Generated by Django 4.0.5 on 2022-06-15 04:06

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CartDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50)),
                ('email', models.TextField(max_length=50)),
                ('phone', models.TextField(max_length=20)),
                ('address', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField(default=0)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 6, 15, 4, 6, 54, 252392))),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='shoeSiteServerApp.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Shoe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=200)),
                ('desc', models.TextField()),
                ('image', models.TextField(max_length=300)),
                ('price', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoes', to='shoeSiteServerApp.category')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField(default=36)),
                ('qty', models.IntegerField(default=0)),
                ('shoe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='shoeSiteServerApp.shoe')),
            ],
        ),
        migrations.CreateModel(
            name='SaleDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shoeSiteServerApp.sale')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shoeSiteServerApp.stock')),
            ],
        ),
        migrations.AddField(
            model_name='sale',
            name='stocks',
            field=models.ManyToManyField(through='shoeSiteServerApp.SaleDetail', to='shoeSiteServerApp.stock'),
        ),
        migrations.AddField(
            model_name='customer',
            name='stocks',
            field=models.ManyToManyField(through='shoeSiteServerApp.CartDetail', to='shoeSiteServerApp.stock'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=200)),
                ('content', models.TextField(max_length=300)),
                ('star', models.IntegerField(default=5)),
                ('shoe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='shoeSiteServerApp.shoe')),
            ],
        ),
        migrations.AddField(
            model_name='cartdetail',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shoeSiteServerApp.customer'),
        ),
        migrations.AddField(
            model_name='cartdetail',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shoeSiteServerApp.stock'),
        ),
        migrations.AddConstraint(
            model_name='saledetail',
            constraint=models.UniqueConstraint(fields=('sale', 'stock'), name='unique_migration_stock_sale'),
        ),
        migrations.AddConstraint(
            model_name='cartdetail',
            constraint=models.UniqueConstraint(fields=('stock', 'customer'), name='unique_migration_stock_customer'),
        ),
    ]