from datetime import datetime, timedelta, timezone
from pprint import pprint
import random
import uuid
import json

import requests

token = '<API Token>'
EnterpriseCustomer = 'customer_id'
StandardCustomer = 'customer_id'
CustomerIds = [EnterpriseCustomer, StandardCustomer]
userId = []

for _ in range(58):
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
for cid in CustomerIds: 
    customerId = cid
    t = datetime.now(timezone.utc) - timedelta(days=33)
    while t < datetime.now(timezone.utc):
        def append_event(event_type, properties):
            events.append({
                "transaction_id": uuid.uuid4().hex,
                "timestamp": t.isoformat(),
                "event_type": event_type,
                "customer_id": customerId,
                "properties": properties,
            })
        if cid == StandardCustomer:
                append_event('gb_logs_ingested', {
                    "gb_ingested":random_monthly_target(10000),
                    "region": random.choice(["eu-west-1","us-east-1"]),
                    "cloud": random.choice(["aws","gcp","azure"])
                })
        if cid == EnterpriseCustomer:
                user_id = uuid.uuid1().fields[1] + random.randint(1,1005)
                append_event('user_login', {
                    "user_id": random.choice(userId),
                    "user_level": random.choice(["admin","user","readOnly"])
                })

        t += timedelta(hours=1)

ingest(events)