# Generated by Django 3.1.5 on 2021-02-18 13:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CustomAdmin', '0002_badgeentries_badges'),
        ('Items', '0003_merge_20210209_1633'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tbl_creativeitems_details',
            name='crt_item_height',
        ),
        migrations.RemoveField(
            model_name='tbl_creativeitems_details',
            name='crt_item_weight',
        ),
        migrations.RemoveField(
            model_name='tbl_creativeitems_details',
            name='crt_item_width',
        ),
        migrations.AddField(
            model_name='tbl_creativeitems_mst',
            name='crt_item_height',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tbl_creativeitems_mst',
            name='crt_item_weight',
            field=models.CharField(blank=True, choices=[('1', 'Below 100g'), ('2', 'Below 250g'), ('3', 'Below 500g'), ('4', 'Below 1kg'), ('5', 'Below 5kg')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='tbl_creativeitems_mst',
            name='crt_item_width',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tbl_creativeitems_mst',
            name='crt_sub_category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='CustomAdmin.tbl_crt_subcategories'),
        ),
        migrations.AlterField(
            model_name='tbl_creativeitems_details',
            name='crt_item_SKU',
            field=models.CharField(max_length=16, unique=True),
        ),
        migrations.AlterField(
            model_name='tbl_creativeitems_details',
            name='crt_item_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='tbl_creativeitems_details',
            name='crt_item_status',
            field=models.CharField(choices=[('INAPPROPRIATE', 'Inappropriate'), ('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('SOLD', 'Sold')], default='ACTIVE', max_length=20),
        ),
        migrations.AlterField(
            model_name='tbl_creativeitems_mst',
            name='crt_item_desc',
            field=models.TextField(default='-'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tbl_crtimages',
            name='crt_img_url',
            field=models.ImageField(max_length=150, null=True, upload_to='item-photos/', validators=[django.core.validators.validate_image_file_extension]),
        ),
        migrations.CreateModel(
            name='tbl_scrapitems',
            fields=[
                ('scp_item_id', models.AutoField(primary_key=True, serialize=False, validators=[django.core.validators.MaxValueValidator(9999999999)])),
                ('scp_item_name', models.CharField(max_length=100)),
                ('scp_item_desc', models.TextField()),
                ('scp_item_price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(1.0)])),
                ('scp_item_qty', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(999)])),
                ('scp_item_SKU', models.CharField(max_length=16, unique=True)),
                ('scp_item_status', models.CharField(choices=[('INAPPROPRIATE', 'Inappropriate'), ('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('SOLD', 'Sold')], default='ACTIVE', max_length=20)),
                ('scp_created_on', models.DateTimeField(auto_now_add=True)),
                ('scp_last_modified', models.DateTimeField(auto_now_add=True)),
                ('scp_sub_category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='CustomAdmin.subscrapcategory')),
            ],
        ),
        migrations.CreateModel(
            name='tbl_scrapimages',
            fields=[
                ('scp_img_id', models.AutoField(primary_key=True, serialize=False, validators=[django.core.validators.MaxValueValidator(99999)])),
                ('scp_img_url', models.ImageField(max_length=150, null=True, upload_to='item-photos/', validators=[django.core.validators.validate_image_file_extension])),
                ('is_primary', models.BooleanField(default=False)),
                ('scp_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Items.tbl_scrapitems')),
            ],
        ),
    ]
