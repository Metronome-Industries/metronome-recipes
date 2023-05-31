# Overview

The folder contains Python3 scripts that show how to generate usage data.

# Pre-requisites

python3 installed

A metronome [API Token](https://docs.metronome.com/using-the-api/authorization/) stored in an `API_TOKEN` environment variable.

Install packages:

```
python3 -m pip install -r requirements.txt
```

# Scripts

- The `generate-usage-GB-Ingested.py` file creates sample usage data in the below format
```
{
  "timestamp": "2022-12-02T03:19:45+00:00",
  "transaction_id": "7115fc41be024c969a4f22a165c767a2",
  "customer_id": "abdc7400-7fb9-457c-858e-8ca12347e0f0",
  "event_type": "gb_logs_ingested",
  "properties": {
    "gb_ingested": "12.7",
    "cloud": "gcp",
    "region": "eu-west-1"
  }
}
```

- The `generate-usage-MAU-data.py` file creates sample usage data in the below format
```
{
  "timestamp": "2022-12-02T03:23:58+00:00",
  "transaction_id": "0c9d7f5a7548448b956fcfe2479461d1",
  "customer_id": "abdc7400-7fb9-457c-858e-8ca12347e0f0",
  "event_type": "user_login",
  "properties": {
    "user_id": "8a0dec9eb3bd48d0ab3f3eb51ecc6b9b",
    "user_level": "admin"
  }
}
```

- The `generate-seats-usage.py` file creates sample seats data in the below format
```
{
  "timestamp": "2022-12-02T03:23:58+00:00",
  "transaction_id": "0c9d7f5a7548448b956fcfe2479461d1",
  "customer_id": "abdc7400-7fb9-457c-858e-8ca12347e0f0",
  "event_type": "account_heartbeat",
  "properties": {
    "developer_seats": 4,
    "developer_seats_in_use": 4,
    "read_only_seats": 20,
    "read_only_seats_in_use": 5
  }
}
```