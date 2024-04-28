# US Border data

This dataset covers data from CBO
making it available as a SQL database.




## Data

### Sources


Sources for multiple csv & pdf from:

- https://www.cbp.gov/newsroom/stats/cbp-public-data-portal

Final data:

- https://www.dolthub.com/repositories/topicalsource/us-border

Clone database to current directory:

```sh
dolt clone topicalsource/us-border .
```

### Schemas

We clean and extend the schemas from the source data

- clean up column names to be lower_snake_case
- add calendar year to pair with fiscal year

See the `./schemas/` directory or
[dolthub/topicalsource/us-border/schema](https://www.dolthub.com/repositories/topicalsource/us-border/schema/main)


### dolt setup

Do this if you have not cloned the dolt database directly.

```sh
# init clean database
dolt init

# apply schemas
dolt sql < schemas/*.sql
```

Serve dolt as a MySQL server

```sh
# run server
dolt sql-server -u ts -p ts -H 0.0.0.0
```


### Tables

We first import the most recent data from csv files.
This is so we can add the newer data to the older
backfills from pdfs.


CSV / latest data:

`python scripts/add_csv_to_table.py --csv <file> --table <table> [--reset,--extend]

```sh
# sbo enc
python scripts/add_csv_to_table.py --csv dl/sbo-encounters-fy19-fy22.csv --table sbo_encounters --reset
python scripts/add_csv_to_table.py --csv dl/sbo-encounters-fy20-fy23.csv --table sbo_encounters --extend
python scripts/add_csv_to_table.py --csv dl/sbo-encounters-fy21-fy24-mar.csv --table sbo_encounters --extend

# nat enc aor
python scripts/add_csv_to_table.py --csv dl/nationwide-encounters-fy20-fy23-aor.csv --table nationwide_encounters_aor --reset
python scripts/add_csv_to_table.py --csv dl/nationwide-encounters-fy21-fy24-mar-aor.csv --table nationwide_encounters_aor --extend

# nat enc state
python scripts/add_csv_to_table.py --csv dl/nationwide-encounters-fy20-fy23-state.csv --table nationwide_encounters_state --reset
python scripts/add_csv_to_table.py --csv dl/nationwide-encounters-fy21-fy24-mar-state.csv --table nationwide_encounters_state --extend
```


PDF / older data:

```sh
# cbp apprehensions
python ./scripts/cbp_apprehensions_monthly.py --reset  # initial
python ./scripts/cbp_apprehensions_monthly.py --extend # newer fill

# nationwide_apprehensions_yearly
python ./scripts/nationwide_apprehensions_yearly.py --reset  # initial
python ./scripts/nationwide_apprehensions_yearly.py --extend # newer fill
```



## Graphs

