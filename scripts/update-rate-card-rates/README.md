# Overview

The folder contains Python3 scripts that show how to update a rate card's prices.

# Pre-requisites

python3 installed

A metronome [API Token](https://docs.metronome.com/using-the-api/authorization/) stored in an `API_TOKEN` environment variable.

Install packages:

```
python3 -m pip install -r requirements.txt
```

# Scripts

The `update-rate-card-rates.py` file will read the specified csv file and execute pricing updates. It will look up current rate cards and products to match.

The example file contains:

- product_name
- price
- rate_type
- entitled
- effective_at
- optional fields which will serve as pricing group keys / values

For example:

```csv
product_name,price,rate_type,entitled,effective_at,resource.provider,resource.region
My product,0,flat,true,2020-10-01T00:00:00.000Z,gcp,uswest2
My product,0,flat,true,2020-10-01T00:00:00.000Z,aws,us-east-2
```

# Usage

API_TOKEN=<your token> python3 ./update-rate-card-rates.py --csv_file ./updates.csv --rate_card_name "Base Rates"
