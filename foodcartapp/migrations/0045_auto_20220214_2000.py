# Generated by Django 3.2 on 2022-02-14 20:00

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0044_alter_order_phone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'пункт заказа', 'verbose_name_plural': 'пункты заказов'},
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(db_index=True, max_length=100, verbose_name='адрес'),
        ),
        migrations.AlterField(
            model_name='order',
            name='firstname',
            field=models.CharField(db_index=True, max_length=50, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='order',
            name='lastname',
            field=models.CharField(db_index=True, max_length=50, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(default=None, max_length=128, region='RU', verbose_name='телефон'),
        ),
    ]
