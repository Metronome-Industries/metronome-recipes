from datetime import datetime, timedelta, timezone
import requests, argparse, os
import json
import random
import uuid
import requests
from dotenv import load_dotenv
load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('--customer_id', type=str, required=True)
parser.add_argument('--events_per_hour', type=int, required=False, default=1)
parser.add_argument('--max_events', type=int, required=False, default=10000000)
parser.add_argument('--days_of_data', type=int, required=False, default=33)
parser.add_argument('--dry_run', type=bool, required=False, default=False)

token = os.getenv('API_TOKEN')
if not token:
    raise ValueError("Set API_TOKEN environment variable to metronome API key")

args = parser.parse_args()
customer_id = args.customer_id
if not customer_id:
    raise ValueError("customer_id must be set")

events_per_hour = args.events_per_hour
if events_per_hour > 1000 or events_per_hour < 1:
    raise ValueError("events_per_hour needs to be greater than 1 and less than 1000")

days_of_data = args.days_of_data
if days_of_data > 33 or days_of_data < 1:
    raise ValueError("days_of_data needs to be greater than 1 and less than 34")

def ingest(events):
    remainder = events
    total_events = len(events)
    total_sent = 0
    start_time = datetime.now()
    while len(remainder) > 0:
        data_to_send = remainder[:100]
        response = requests.post(
            "https://api.staging.metronome.com/v1/ingest",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json=data_to_send
        )
        if response.status_code != 200:
            print(f'ERROR {response.status_code}: {response.text}')
        else:
            total_sent += len(data_to_send)
        remainder = remainder[100:]
    
    end_time = datetime.now()
    print(f"total events: {total_events} sent: {total_sent}")
    duration_seconds = (end_time - start_time).total_seconds()
    duration_minutes = duration_seconds / 60
    print(f"start time: {start_time}")
    print(f"end time: {end_time}")
    print(f"total time: {duration_seconds} seconds or {duration_minutes} minutes")

def random_monthly_target(n):
    return random.randint(90*n // 720, 110*n // 720) / 100

events = []
t = datetime.now(timezone.utc) - timedelta(days=days_of_data)
while t < datetime.now(timezone.utc):
    def append_event(event_type, properties):
        events.append({
            "transaction_id": uuid.uuid4().__str__() + "-" + str(len(events)),
            "timestamp": t.isoformat(),
            "event_type": event_type,
            "customer_id": customer_id,
            "properties": properties,
        })
    for index in range(events_per_hour):
        append_event('gb_logs_ingested', {
                "gb_ingested":random_monthly_target(10000),
                "region": random.choice(["eu-west-1","us-east-1"]),
                "cloud": random.choice(["aws","gcp","azure"])
        })
    t += timedelta(hours=1)

events = events[:args.max_events]
if args.dry_run:
    print("dry_run, not ingesting events.  Event count:")
    print(len(events))

    if len(events) < 50:
        print("the events:")
        print(json.dumps(events, indent=2))
else:
    ingest(events)
