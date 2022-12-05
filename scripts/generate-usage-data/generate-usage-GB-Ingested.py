from datetime import datetime, timedelta, timezone
from pprint import pprint
import requests, argparse, os
import random
import uuid
import requests
from dotenv import load_dotenv
load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('--customer_id', type=str, required=True)
parser.add_argument('--days_of_data', type=int, required=False, default=33)

token = os.getenv('API_TOKEN')
if not token:
    raise ValueError("Set API_TOKEN environment variable to metronome API key")

args = parser.parse_args()
customer_id = args.customer_id
if not customer_id:
    raise ValueError("customer_id must be set")

days_of_data = args.days_of_data
if days_of_data > 33 or days_of_data < 1:
    raise ValueError("days_of_data needs to be greater than 1 and less than 34")


def ingest(events):
    remainder = events
    while len(remainder) > 0:
        pprint(remainder[:100])

        response = requests.post(
            "https://api.metronome.com/v1/ingest",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json=remainder[:100]
        )
        if response.status_code != 200:
            print(f'ERROR {response.status_code}: {response.text}')
        remainder = remainder[100:]

def random_monthly_target(n):
    return random.randint(90*n // 720, 110*n // 720) / 100

events = []
t = datetime.now(timezone.utc) - timedelta(days=days_of_data)
while t < datetime.now(timezone.utc):
    def append_event(event_type, properties):
        events.append({
            "transaction_id": uuid.uuid4().hex,
            "timestamp": t.isoformat(),
            "event_type": event_type,
            "customer_id": customer_id,
            "properties": properties,
        })
    append_event('gb_logs_ingested', {
            "gb_ingested":random_monthly_target(10000),
            "region": random.choice(["eu-west-1","us-east-1"]),
            "cloud": random.choice(["aws","gcp","azure"])
    })
    t += timedelta(hours=1)

ingest(events)