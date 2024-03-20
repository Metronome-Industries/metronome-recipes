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

- rate_card_name
- product_name
- price
- rate_type
- entitled
- effective_at
- pricing_group_values

For example:

```csv
rate_id,rate_card_id,rate_card_name,product_id,product_name,price,rate_type,entitled,effective_at,pricing_group_values
rate_00b4b05fb03063fdfdb8659546eac0fcd7a813a61ece4dfeb1f9226f8cdc8998,rate_card_40e1111a53098cdb1abd6919f9d0c3e80d5ce23368cabc1eaf6e728e6df7d729,Confluent Base Rates,product_01a5d1b747ee119aaac52187259bcf7527bf404fce3f2c6ccbfd2c5e4a67975b,GovernanceBase,0,flat,true,2020-10-01T00:00:00.000Z,"{""resource.provider"":""gcp"",""resource.region"":""us-central1"",""resource.package"":""free""}"
rate_012f37b5b409d5dd9434729a73983486daaeb04bac0367a1fa4fe7554c6cecaf,rate_card_40e1111a53098cdb1abd6919f9d0c3e80d5ce23368cabc1eaf6e728e6df7d729,Confluent Base Rates,product_01a5d1b747ee119aaac52187259bcf7527bf404fce3f2c6ccbfd2c5e4a67975b,GovernanceBase,0,flat,true,2020-10-01T00:00:00.000Z,"{""resource.provider"":""gcp"",""resource.region"":""asia-south1"",""resource.package"":""free""}"
```

# Usage

API_TOKEN=<your token> python3 ./update-rate-card-rates.py --csv_file ./updates.csv
