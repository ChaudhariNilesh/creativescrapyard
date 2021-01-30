# Generated by Django 3.1.4 on 2021-01-24 12:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Items', '0006_auto_20210120_1104'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_creativeitems_details',
            fields=[
                ('crt_item_details_id', models.PositiveIntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MaxValueValidator(9999999999)])),
                ('crt_item_color', models.CharField(max_length=7)),
                ('crt_item_size', models.CharField(blank=True, choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')], max_length=3, null=True)),
                ('crt_item_price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('crt_item_qty', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(999)])),
                ('crt_item_weight', models.CharField(blank=True, choices=[('Below 100g', 'Below 100g'), ('Below 250g', 'Below 250g'), ('Below 500g', 'Below 500g'), ('Below 1kg', 'Below 1kg'), ('Below 5kg', 'Below 5kg')], max_length=10, null=True)),
                ('crt_item_height', models.DecimalField(decimal_places=2, max_digits=5)),
                ('crt_item_width', models.DecimalField(decimal_places=2, max_digits=5)),
                ('crt_item_SKU', models.CharField(max_length=16)),
                ('crt_item_status', models.CharField(choices=[('INAPPROPRIATE', 'Inappropriate'), ('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('SOLD', 'Sold')], default='INACTIVE', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='tbl_creativeitems_mst',
            fields=[
                ('crt_item_id', models.PositiveIntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MaxValueValidator(9999999999)])),
                ('crt_item_name', models.CharField(max_length=100)),
                ('crt_item_desc', models.TextField(blank=True, null=True)),
                ('crt_created_on', models.DateTimeField(auto_now_add=True)),
                ('crt_last_modified', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='tbl_crtimages',
            fields=[
                ('crt_img_id', models.PositiveIntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MaxValueValidator(99999)])),
                ('crt_img_url', models.ImageField(max_length=150, null=True, upload_to='photos/')),
                ('is_primary', models.BooleanField(default=False)),
                ('crt_item_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Items.tbl_creativeitems_details')),
            ],
        ),
        migrations.AddField(
            model_name='tbl_creativeitems_details',
            name='crt_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Items.tbl_creativeitems_mst'),
        ),
    ]
