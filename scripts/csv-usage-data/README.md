# Overview

The folder contains a Python3 script that takes data from a csv file and sends it into Metronome via the [Ingest events](https://docs.metronome.com/api/#operation/ingest) endpoint.

# Pre-requisites

python3 installed

A metronome [API Token](https://docs.metronome.com/using-the-api/authorization/) stored in an `API_TOKEN` environment variable.

Install packages:

```
python3 -m pip install -r requirements.txt
```

A csv file of data in the same folder as the `usage_csv.py` script. 

# Scripts

- The `usage_csv.py` file creates sample usage data in the below format
```
{
  "timestamp": "2022-12-02T03:19:45+00:00",
  "transaction_id": "7115fc41be024c969a4f22a165c767a2",
  "customer_id": "abdc7400-7fb9-457c-858e-8ca12347e0f0",
  "event_type": "gb_logs_ingested",
  "properties": {
    "property1": "value",
    "property2": "value",
    "property3": "value"
  }
}
```

The script will also output a csvfile (`output.csv`) of the data sent into Metronome with `transaction_ids` and `timestamps` for each event. 

# CSV file

The csv file must be in the same folder as the `usage_csv.py` script. The csv should have the property headers as the first row. For customer_id, you can either add it to the csv or specify it as a command line argument.