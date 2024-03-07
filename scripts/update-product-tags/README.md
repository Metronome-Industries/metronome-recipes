# Overview

The folder contains Python3 scripts that show how to update a contract products tags and custom fields.

# Pre-requisites

python3 installed

A metronome [API Token](https://docs.metronome.com/using-the-api/authorization/) stored in an `API_TOKEN` environment variable.

Install packages:

```
python3 -m pip install -r requirements.txt
```

# Scripts

The `update-product-tags.py` file will read the specified csv file and ensure custom fields and tags are associated with the give products

The example file contains:

- Product name
- effective date for the change
- tags column
- Field:field-name columns

For example:

```csv
product_name,effective_at,tags,field:unique_id,field:unit
my test product 1,2022-01-01T00:00:00Z,"tag_1,tag_2",prod1_id,GB
my test product 2,2020-01-01T00:00:00Z,"tag_3",prod2_id,Minutes
```

The script will create the following custom fields if they do not exist:

- unique_id
- unit

The script will use current product name and will update the product's tags / custom fields.

# Usage

API_TOKEN=<your token> python3 ./update-product-tags.py --csv_file ./product-tags.csv
