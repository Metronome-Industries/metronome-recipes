# databricks/netsuite charge custom fields uploader

This is a python script to help set custom fields on charges for customers with downstream integrations.  It was originally developed to help with databricks and their netsuite integration.  Databricks provides us with a spreadsheet containing billable metric (charge) name and netsuite internal id, and we use that to set the appropriate custom field on each charge for them.


## how to run this script

- Make sure you have python 3 installed
- create a virtual environment with `python3 -m venv venv`
- activate the virtual environment `. venv/bin/activate`
- install dependencies `pip install -r requrements.txt`
- get an impersonation token and set it to the `TOKEN` variable in `main.py`
- verify that the other constants at the top of `main.py` point to the correct csv files and column headers
- run the script `python main.py`

## csv files you will need

1. A csv from a client with charge names and netsuite internal ids. 
    - There is an example csv `internal_ids_example.csv` in this repo. 
    - If the csv you have looks different than the one that already exists in this repo, update the `DB_BILLABLE_METRIC_NAME_HEADER` and `DB_NETSUITE_INTERNAL_ID_HEADER` variables at the top of `main.py`
        - `DB_BILLABLE_METRIC_NAME_HEADER` = the header name of the column with billable metric name.  With databricks, sometimes they send a column that's prefixed with PAYGO and one without.  You want the one _not_ prefixed with PAYGO so it'll match to our data
        - `DB_NETSUITE_INTERNAL_ID_HEADER` = the header name of the column with netsuite (or other intgration) internal id
    
2. A csv with all of the  charge ids
    - This csv is `charges_example.csv` in this repo
    - The example was generated using the following `psql` command, which can be modified to suit your use case:
        - `\copy (select ppf.id as charge_id, ppf.name as charge_name, p.id as product_id, p.name as product_name, p.environment_type from "ProductPricingFactor" ppf join "Product" p on ppf.product_id = p.id where p.id = '5a6e8e89-aae2-45b0-b1e3-97f46c652f8e') to ~/Desktop/databricks_charges.csv csv header;`
