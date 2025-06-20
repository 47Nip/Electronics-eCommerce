# Generated by Django 5.0.7 on 2024-10-20 06:05

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0002_filter_price_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter_price',
            name='price',
            field=models.CharField(choices=[('1000 TO 10000', '1000 TO 10000'), ('10000 TO 20000', '10000 TO 20000'), ('20000 TO 30000', '20000 TO 30000'), ('30000 TO 40000', '30000 TO 40000'), ('40000 TO 50000', '40000 TO 50000')], max_length=60),
        ),
        migrations.CreateModel(
            name='PRODUCT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('image', models.ImageField(upload_to='product_image/img')),
                ('name', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('condition', models.CharField(choices=[('New', 'New'), ('Old', 'Old')], max_length=100)),
                ('information', models.TextField()),
                ('description', models.TextField()),
                ('stock', models.CharField(choices=[('IN STOCK ', 'IN STOCK'), ('OUT OF STOCK', 'OUT OF STOCK')], max_length=200)),
                ('status', models.CharField(choices=[('Publish', 'Publish'), ('Draft', 'Draft')], max_length=200)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store_app.brand')),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store_app.categories')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store_app.color')),
                ('filter_Price', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store_app.filter_price')),
            ],
        ),
    ]
