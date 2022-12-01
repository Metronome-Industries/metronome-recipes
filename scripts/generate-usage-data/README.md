# Overview

Python3 script which shows how to generate usage data for two customers.

# Pre-requisites

python3 installed

A metronome [API Token](https://docs.metronome.com/using-the-api/authorization/) added to the script.
```
token = '<API Token>'
```

Install packages:

```
python3 -m pip install -r requirements.txt
```

# Scripts

## generate-usage-data

This script generates usage data for two customers (`EnterpriseCustomer`, `StandardCustomer`) who can be on two plan types.

```
python3 ./generate-usage-data.py 
```
For the `EnterpriseCustomer` the usage events look like:
```
{
  "timestamp": "2022-12-01T17:29:54+00:00",
  "transaction_id": "abc123c28b2cb34dac8cbf0b9c30cedf95",
  "customer_id": "abcd1234-70b9-476c-9ef9-78064157ff5f",
  "event_type": "gb_logs_ingested",
  "properties": {
    "gb_ingested": "1234",
    "region": "eu-west-1",
    "cloud": "aws"
  }
}
```

For the `StandardCustomer` the usage events look like:
```
{
  "timestamp": "2022-12-01T17:29:54+00:00",
  "transaction_id": "abc123c28b2cb34dac8cbf0b9c30cedf95",
  "customer_id": "abcd1234-70b9-476c-9ef9-78064157ff5f",
  "event_type": "gb_logs_ingested",
  "properties": {
    "user_id": "f7aa97e8f34349df8070ea1c8793d109",
    "user_level": "admin"
  }
}
```