from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from phonenumbers import is_valid_number, parse
import json

from .models import Product
from .models import Order
from .models import OrderItem


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(["POST"])
def register_order(request):
    order_payload = request.data
    order_keys = ('firstname', 'lastname', 'phonenumber', 'address')
    try:
        if 'products' not in order_payload:
            raise KeyError('products: Обязательное поле.')
        products = order_payload['products']
        for key in order_keys:
            if key not in order_payload:
                raise KeyError(
                    'firstname, lastname, phonenumber, address: Обязательное поле.'
                )
        for key in order_keys:
            if isinstance(key, type(None)):
                raise ValueError(
                    'firstname, lastname, phonenumber, address: Это поле не может быть пустым.'
                )
        if isinstance(products, type(None)):
            raise ValueError(
                'products: Это поле не может быть пустым.'
            )
        if bool(products) is False:
            raise ValueError('products: Этот список не может быть пустым.')
        if isinstance(products, str):
            raise ValueError(
                'products: Ожидался list со значениями, но был получен "str"'
            )
        if isinstance(order_payload['firstname'], type(None)):
            raise ValueError(
                'firstname: Это поле не может быть пустым.'
            )
        if bool(order_payload['phonenumber']) is False:
            raise ValueError(
                'phonenumber: Это поле не может быть пустым.'
            )
        phonenumber_obj = parse(order_payload['phonenumber'], 'RU')
        if not is_valid_number(phonenumber_obj):
            raise ValueError(
                'phonenumber: Введен некорректный номер телефона.'
            )
        product_ids = Product.objects.values_list('id', flat=True)
        for item in products:
            if item['product'] not in product_ids:
                raise ValueError(
                    f'products: Недопустимый первичный ключ {item["product"]}'
                )
        if isinstance(order_payload['firstname'], list):
            raise ValueError(
                'firstname: Not a valid string.'
            )
    except KeyError as error:
        return Response(
            data=error.args,
            status=status.HTTP_400_BAD_REQUEST
        )
    except ValueError as error:
        return Response(
            data=error.args,
            status=status.HTTP_400_BAD_REQUEST
        )
    order = Order.objects.create(
        firstname=order_payload['firstname'],
        lastname=order_payload['lastname'],
        phone=order_payload['phonenumber'],
        address=order_payload['address']
    )
    for item in products:
        OrderItem.objects.create(
            order=order,
            product=Product.objects.get(id=item['product']),
            quantity=item['quantity']
        )
    return Response('Sucсess')
