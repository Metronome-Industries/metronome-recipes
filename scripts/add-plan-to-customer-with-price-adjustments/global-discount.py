import requests, argparse, os
from dateutil.parser import parse

parser = argparse.ArgumentParser()
parser.add_argument('--customer_id', type=str, required=True)
parser.add_argument('--plan_id', type=str, required=True)
parser.add_argument('--discount_percentage', type=float, required=True)
parser.add_argument('--starting_on', type=parse, required=True)
parser.add_argument('--ending_before', type=parse, required=False)

token = os.getenv('API_TOKEN')
if not token:
    raise ValueError("Set API_TOKEN environment variable to metronome API key")

args = parser.parse_args()
customer_id = args.customer_id
if not customer_id:
    raise ValueError("customer_id must be set")

plan_id = args.plan_id
if not plan_id:
    raise ValueError("plan_id must be set")

discount_percentage = args.discount_percentage
if not discount_percentage:
    raise ValueError("discount_percentage must be set")

starting_on = args.starting_on
if not starting_on:
    raise ValueError("starting_on must be set")
starting_on = starting_on.isoformat().replace("+00:00", "Z")

ending_before = args.ending_before
if ending_before:
    ending_before = ending_before.isoformat().replace("+00:00", "Z")

nextPage = ""
url = f"https://api.metronome.com/v1/planDetails/{plan_id}/charges"
params = {'next_page': nextPage}
charges = []

response = requests.get(
    url, 
    params=params,
    headers={
        "Authorization": f"Bearer {token}",
    },
)
jsonResponse = response.json()
for charge in jsonResponse["data"]:
  for price in charge["prices"]:
    charges.append({ "id": charge["id"], "start_period": charge["start_period"], "tier": price["tier"] })

nextPage = jsonResponse["next_page"]
while nextPage is not None:
  params = {'next_page': nextPage}
  response = requests.get(
    url, 
    params=params,
    headers={
      "Authorization": f"Bearer {token}",
      },
      )
  jsonResponse = response.json()
  for charge in jsonResponse["data"]:
    for price in charge["prices"]:
      charges.append({ "id": charge["id"], "start_period": charge["start_period"], "tier": price["tier"] })
  nextPage = jsonResponse["next_page"]

adjustments = []
for charge in charges:
  adjustments.append({"charge_id":charge["id"],"adjustment_type":"percentage", "value":discount_percentage, "start_period":charge["start_period"], "tier":charge["tier"]})

response = requests.post(
    f"https://api.metronome.com/v1/customers/{customer_id}/plans/add",
    headers={
        "Authorization": f"Bearer {token}",
    },
    json={
        "plan_id": plan_id,
        "starting_on": starting_on,
        "ending_before": ending_before,
        "price_adjustments": adjustments
    },
)
if response.status_code != 200:
  print(response.text)
else: 
  print("Plan created")