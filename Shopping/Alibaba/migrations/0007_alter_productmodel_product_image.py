# Generated by Django 4.2.11 on 2024-04-29 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alibaba', '0006_alter_productmodel_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='product_image',
            field=models.ImageField(blank=True, null=True, upload_to='proImage'),
        ),
    ]
