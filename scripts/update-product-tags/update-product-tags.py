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

load_dotenv()  # take environment variables from .env.

parser = argparse.ArgumentParser()
parser.add_argument('--csv_file', type=str, help='CSV file with product data')

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

# retrieve custom field keys
# https://docs.metronome.com/api/#operation/listCustomFieldKeys
response = requests.post(
    f"{api_url}/v1/customFields/listKeys",
    headers=headers,
    json={
        "entities": [
            "contract_product"
        ]
    },
)
response.raise_for_status()

current_custom_fields = {}
for custom_field in response.json()['data']:
    current_custom_fields[custom_field['key']] = custom_field

# read all products and their current custom fields / tags
productHash = {}
next_page = None
print('retrieving current products and their custom fields and tags')
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
            'tags': current['tags'],
            'custom_fields': product['custom_fields']
        }

    next_page = response_json['next_page']

    if not next_page:
        break

# read the csv file and build to product => custom fields and tags hash
product_updates = []

with open(csv_file_path) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')

    # check for custom field columns, create if not found
    custom_field_columns = []
    for column in csv_reader.fieldnames:
        if column.startswith('field:'):
            print(f"Custom field column found: {column}")
            custom_field = column.split(':')[1]
            custom_field_columns.append(custom_field)

            if custom_field not in current_custom_fields:
                print(
                    f"Custom field {custom_field} not found in Metronome, creating")
                custom_field_create_response = requests.post(
                    f"{api_url}/v1/customFields/addKey",
                    headers=headers,
                    json={
                        "key": custom_field,
                        "entity": "contract_product",
                        "enforce_uniqueness": False
                    }
                )
                custom_field_create_response.raise_for_status()

    for row in csv_reader:
        product_name = row['product_name']
        tags = row['tags'].split(',')
        effective_at = row['effective_at']

        if product_name not in productHash:
            print(f"Product {product_name} not found")
            continue

        product = productHash[product_name]
        product_id = product['id']

        custom_field_values = {}
        for custom_field in custom_field_columns:
            custom_field_values[custom_field] = row[f'field:{custom_field}']

        print('processing product: ', product_name, 'id: ', product_id)

        # set the custom tags
        print('setting custom tags')
        response = requests.post(
            f"{api_url}/v1/customFields/setValues",
            headers=headers,
            json={
                "entity": "contract_product",
                "entity_id": product_id,
                "custom_fields": custom_field_values
            },
        )
        response.raise_for_status()

        # if product tags are not all there, then update the product
        if not all(tag in product['tags'] for tag in tags):
            print('updating tags')
            response = requests.post(
                f"{api_url}/v1/contract-pricing/products/update",
                headers=headers,
                json={
                    "product_id": product_id,
                    "tags": tags,
                    "starting_at": effective_at,
                }
            )
            response.raise_for_status()
        else:
            print('tags already set')

print('done processing products and tags')
