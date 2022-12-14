from datetime import datetime, timedelta, timezone
from pprint import pprint
import requests, argparse, os
import random
import uuid
import os
import csv
import json
import re 
import random

import requests
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('--days_of_data', type=int, required=False, default=33)
parser.add_argument('--customer_id', type=str, required=False)
parser.add_argument('--event_type', type=str, required=False, default="event_type")
parser.add_argument('--filename', type=str, required=True, default="example_usage.csv")

token = os.getenv('API_TOKEN')
if not token:
    raise ValueError("Set API_TOKEN environment variable to metronome API key")

args = parser.parse_args()
customer_id = args.customer_id

days_of_data = args.days_of_data
if days_of_data > 33 or days_of_data < 1:
    raise ValueError("days_of_data needs to be greater than 1 and less than 33")

filename = args.filename
if not isinstance(filename, str):
    raise ValueError("filename must be a string")

event_type = args.event_type
if not isinstance(event_type, str):
    raise ValueError("event_type must be a string")


csvFilePath = "./"+filename
hours_of_data = days_of_data*24
total_events= []

with open(csvFilePath) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    list_of_column_names = []
    for row in csv_reader:
        list_of_column_names.append(row)
        break

def make_json(csvFilePath):
    data = []
     
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        for rows in csvReader:
             
            data.append(rows)
        for items in data:
            time_delta = random.randint(0,hours_of_data)
            t = datetime.now(timezone.utc) - timedelta(hours=time_delta)
            properties = {}
            itemforproperties = {}
            for propertiesItems in list_of_column_names[0]:
                if str(propertiesItems) == "customer_id":
                    customer_id = items[propertiesItems]
                else:
                    properties[str(propertiesItems)]=items[str(propertiesItems)] 

                event = {
                    "timestamp": t.isoformat(),
                    "transaction_id": uuid.uuid4().hex,
                    "customer_id": customer_id,
                    "event_type": event_type,
                    "properties": properties
                }
            total_events.append(event)


make_json(csvFilePath)

jsondata = total_events
 
data_file = open('output.csv', 'w', newline='')
csv_writer = csv.writer(data_file)
 
count = 0
headervalues = []
for data in jsondata:
    for item in data:
        if count == 0:
            header = data.keys() 
            headervalues = list(header)+list(data['properties'].keys())
            headervalues.remove('properties')
            csv_writer.writerow(headervalues)
            count += 1
        else:
            row = data.values()
            rowList = list(row)
            propertyRowValues = list(data['properties'].values())
            rowList.pop(len(rowList)-1)
            rowvalues = rowList+propertyRowValues
            csv_writer.writerow(rowvalues)
            count += 1 
data_file.close()


def ingest(events):
    remainder = events
    while len(remainder) > 0:
        #pprint(remainder[:100])

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

events = total_events

ingest(events)

