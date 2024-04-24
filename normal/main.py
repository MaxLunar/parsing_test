import json
import itertools
import requests

base_url = 'https://www.auchan.ru'
api_endpoint = '/v1/catalog/products'

def get_products(category):
    buffer = {}
    for n in itertools.count(1):
        response = requests.post(base_url+api_endpoint,
            params={
                'merchantId': 1,
                'page': n,
                'perPage': 100,
                'deliveryAddressSelected': 0,
            },
            json={'filter': {
                'category': category,
                'promo_only': False,
                'active_only': True,
                'cashback_only': False
            }}
        )
        j = response.json()
        if len(j['items']):
            for item in j['items']:
                buffer[item['id']] = {
                    'name': item['title'],
                    'url': f'{base_url}/product/{item["code"]}/',
                    'price': item['price'],
                    'old_price': item['oldPrice'],
                    'brand': item["brand"],
                }
        else:
            break
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(buffer, f, indent=4, ensure_ascii=False)

get_products('salaty-zakuski-humus')