# Generated by Django 4.2.11 on 2024-05-07 10:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Alibaba', '0011_alter_customermodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customermodel',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterUniqueTogether(
            name='customermodel',
            unique_together={('user',)},
        ),
    ]
