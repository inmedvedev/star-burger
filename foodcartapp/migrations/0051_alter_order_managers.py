# Generated by Django 3.2 on 2022-02-17 23:30

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0050_order_is_processed'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='order',
            managers=[
                ('price', django.db.models.manager.Manager()),
            ],
        ),
    ]
