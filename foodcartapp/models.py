from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import F, Sum, Prefetch
from datetime import datetime
from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )
    lng = models.FloatField('Долгота')
    lat = models.FloatField('Широта')

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=600,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def get_order_price(self):
        return self.annotate(
            order_price=Sum(
                F('items__quantity')*F('items__price')
            )
        )


class Order(models.Model):
    IS_PROCESSED_CHOICES = [
        (True, 'Обработанный'),
        (False, 'Необработанный'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличными'),
        ('non-cash', 'Безналичный расчет'),
        ('by card', 'Картой при получении')
    ]
    firstname = models.CharField(
        'название',
        max_length=50,
        db_index=True
    )
    lastname = models.CharField(
        'название',
        max_length=50,
        db_index=True
    )
    phonenumber = PhoneNumberField('телефон', region='RU')
    address = models.CharField(
        'адрес',
        max_length=100,
        db_index=True
    )
    is_processed = models.BooleanField(
        'обработан',
        default=False,
        choices=IS_PROCESSED_CHOICES,
        db_index=True
    )
    comment = models.TextField(
        'комментарий',
        blank=True
    )
    registered_at = models.DateTimeField(
        default=timezone.now,
        db_index=True
    )
    called_at = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
        db_index=True
    )
    delivered_at = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
        db_index=True
    )
    payment_method = models.CharField(
        'способ оплаты',
        max_length=100,
        choices=PAYMENT_METHOD_CHOICES,
        db_index=True
    )
    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f"{self.firstname} {self.lastname} {self.address}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        verbose_name='заказ',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        verbose_name='продукт',
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(
        'количество',
        validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(
        'цена товара',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'пункт заказа'
        verbose_name_plural = 'пункты заказа'

    def __str__(self):
        return f"{self.product} {self.quantity}"
