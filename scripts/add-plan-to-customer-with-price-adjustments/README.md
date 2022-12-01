# Overview

Python3 scripts which show how to apply adjustments to a customer.

# Pre-requisites

python3 installed

A metronome [API Token](https://docs.metronome.com/using-the-api/authorization/) stored in an `API_TOKEN` environment variable.

Install packages:

```
python3 -m pip install -r requirements.txt
```

# Scripts

## global-discount

Applies a global discount to a customer. The global percentage applied to a cost, for example, -.1 for a global 10% discount or .1 for a global 10% increase.

```
python3 ./global-discount.py \
    --plan_id d7abd0cd-4ae9-4db7-8676-e986a4ebd8dc \
    --customer_id d776066c-36cd-4782-a9a2-1467ca7e5e1f \
    --discount_percentage .21 \
    --starting_on 2022-11-23T00:00:00Z \
    --ending_before 2022-12-31T00:00:00Z
```
