# Generated by Django 3.2 on 2022-02-14 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0040_auto_20220214_0047'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'заказ', 'verbose_name_plural': 'заказы'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='foodcartapp.order', verbose_name='заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='foodcartapp.product', verbose_name='продукт')),
            ],
        ),
    ]
