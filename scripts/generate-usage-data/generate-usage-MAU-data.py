from datetime import datetime, timedelta, timezone
from pprint import pprint
import requests, argparse, os
import random
import uuid
import json
import requests
from dotenv import load_dotenv
load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('--customer_id', type=str, required=True)
parser.add_argument('--number_of_MAUs', type=int, required=False, default=75)

token = os.getenv('API_TOKEN')
if not token:
    raise ValueError("Set API_TOKEN environment variable to metronome API key")

args = parser.parse_args()
customer_id = args.customer_id
if not customer_id:
    raise ValueError("customer_id must be set")

number_of_MAUs = args.number_of_MAUs
if number_of_MAUs > 200 or number_of_MAUs < 1:
    raise ValueError("number_of_MAUs needs to be greater than 1 and less than 200")

userId = []

for _ in range(number_of_MAUs):
    userId.append(uuid.uuid4().hex)

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
    return random.randint(n, 2*n)

events = []
t = datetime.now(timezone.utc) - timedelta(days=33)
while t < datetime.now(timezone.utc):
    def append_event(event_type, properties):
        events.append({
            "transaction_id": uuid.uuid4().hex,
            "timestamp": t.isoformat(),
            "event_type": event_type,
            "customer_id": customer_id,
            "properties": properties,
        })
    append_event('user_login', {
        "user_id": random.choice(userId),
        "user_level": random.choice(["admin","user","readOnly"])
    })

    t += timedelta(hours=1)

ingest(events)