import csv
import requests
import concurrent.futures

API_URL = "https://api.metronome.com"
TOKEN = ""
INTERNAL_ID_CSV = "internal_ids_example.csv"
INTERNAL_ID_CSV_CHARGE_NAME_HEADER = "Billable metric name"
INTERNAL_ID_CSV_INTERNAL_ID_HEADER = "NetSuite Internal ID"
CHARGES_CSV = "charges_example.csv"
CHARGES_CSV_CHARGE_NAME_HEADER = "charge_name"
CHARGES_CSV_CHARGE_ID_HEADER = "charge_id"
CUSTOM_FIELD_NAME = "netsuite_internal_item_id"

def make_request(request_body):
    try:
        response = requests.post(
            f"{API_URL}/v1/customFields/setValues",
            json=request_body,
            headers={"Authorization": f"Bearer {TOKEN}"},
        )
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to set custom fields for charge id {request_body['entity_id']}")
        print(e)


def main():
    charge_name_to_id = {}

    with open(CHARGES_CSV) as file:
        charges = csv.DictReader(file)
        for row in charges:
            charge_name_to_id[row[CHARGES_CSV_CHARGE_NAME_HEADER]] = row[CHARGES_CSV_CHARGE_ID_HEADER]

    request_bodies = []

    with open(INTERNAL_ID_CSV) as file:
        custom_fields = csv.DictReader(file)
        for row in custom_fields:
            try:
                charge_id = charge_name_to_id[row[INTERNAL_ID_CSV_CHARGE_NAME_HEADER]]
                request_bodies.append(
                    {
                        "entity": "charge",
                        "entity_id": charge_id,
                        "custom_fields": {
                            [CUSTOM_FIELD_NAME]: row[
                                INTERNAL_ID_CSV_INTERNAL_ID_HEADER
                            ],
                        },
                    }
                )
            except KeyError:
                print(
                    f"Charge id does not exist for {row[INTERNAL_ID_CSV_CHARGE_NAME_HEADER]}"
                )

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(make_request, request_bodies)


main()
