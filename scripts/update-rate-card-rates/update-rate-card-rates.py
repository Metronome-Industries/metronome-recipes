from datetime import datetime, timedelta, timezone
from pprint import pprint
import requests
import argparse
import os
import csv
import random
import uuid
import requests
from dotenv import load_dotenv
from collections import defaultdict
import json

load_dotenv()  # take environment variables from .env.

parser = argparse.ArgumentParser()
parser.add_argument('--csv_file', type=str, help='CSV file with rate data')

token = os.getenv('API_TOKEN')
if not token:
    raise ValueError("Set API_TOKEN environment variable to metronome API key")

args = parser.parse_args()
csv_file_path = args.csv_file
if not csv_file_path:
    raise ValueError("csv_file must be set")

api_url = os.getenv('API_URL', 'https://api.metronome.com')

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# read all products and their current custom fields / tags
productHash = {}
next_page = None
print('retrieving current products')
while True:
    next_page_param = f"&next_page={next_page}" if next_page else ""
    response = requests.post(
        f"{api_url}/v1/contract-pricing/products/list?limit=100{next_page_param}",
        headers=headers,
        json={}
    )
    response.raise_for_status()

    response_json = response.json()
    response_data = response_json['data']
    for product in response_data:
        current = product['current']
        productHash[current['name']] = {
            'id': product['id'],
        }

    next_page = response_json['next_page']

    if not next_page:
        break

rateCardHash = {}
next_page = None
print('retrieving current rate cards')
while True:
    next_page_param = f"&next_page={next_page}" if next_page else ""
    response = requests.post(
        f"{api_url}/v1/contract-pricing/rate-cards/list?limit=100{next_page_param}",
        headers=headers,
        json={}
    )
    response.raise_for_status()

    response_json = response.json()
    response_data = response_json['data']
    for rate_card in response_data:
        rateCardHash[rate_card['name']] = {
            'id': rate_card['id'],
        }

    next_page = response_json['next_page']

    if not next_page:
        break


rates_to_send_by_rate_card = defaultdict(list)
with open(csv_file_path) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')

    for row in csv_reader:
        rate_card_name = row['rate_card_name']
        product_name = row['product_name']
        effective_at = row['effective_at']
        pricing_group_values_str = row['pricing_group_values']
        pricing_group_values = None
        if pricing_group_values_str:
            pricing_group_values = json.loads(pricing_group_values_str)

        entitled = row['entitled']
        rate_type = row['rate_type']
        price = float(row['price'])

        if rate_card_name not in rateCardHash:
            print(f"Rate card {rate_card_name} not found")
            continue

        rate_card = rateCardHash[rate_card_name]
        rate_card_id = rate_card['id']

        if product_name not in productHash:
            print(f"Product {product_name} not found")
            continue

        product = productHash[product_name]
        product_id = product['id']

        rates_to_send_by_rate_card[rate_card_id].append({
            'product_id': product_id,
            'effective_at': effective_at,
            'pricing_group_values': pricing_group_values,
            'starting_at': effective_at,
            'entitled': entitled.lower() == 'true',
            'rate_type': rate_type,
            'price': price,
        })

batch_size = 100
for rate_card_id, rates_to_send in rates_to_send_by_rate_card.items():
    print(
        f"processing {len(rates_to_send)} rates for rate card {rate_card_id}")
    remainder = rates_to_send
    total_rates = len(rates_to_send)
    total_sent = 0
    start_time = datetime.now()
    while len(remainder) > 0:
        data_to_send = remainder[:batch_size]
        response = requests.post(
            f"{api_url}/v1/contract-pricing/rate-cards/addRates",
            headers=headers,
            json={
                "rate_card_id": rate_card_id,
                "rates": data_to_send
            }
        )
        if response.status_code != 200:
            print(f'ERROR {response.status_code}: {response.text}')
        else:
            total_sent += len(data_to_send)
        remainder = remainder[batch_size:]

    end_time = datetime.now()
    print(f"total rates: {total_rates} sent: {total_sent}")
    duration_seconds = (end_time - start_time).total_seconds()
    duration_minutes = duration_seconds / 60
    print(f"start time: {start_time}")
    print(f"end time: {end_time}")
    print(
        f"total time: {duration_seconds} seconds or {duration_minutes} minutes")

print('done processing rates')
