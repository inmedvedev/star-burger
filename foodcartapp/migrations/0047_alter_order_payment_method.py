# Generated by Django 3.2 on 2022-02-19 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0046_alter_order_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Наличными'), ('non-cash', 'Безналичный расчет'), ('by card', 'Картой при получении')], max_length=100, verbose_name='способ оплаты'),
        ),
    ]
