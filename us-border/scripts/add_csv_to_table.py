import pandas as pd

from util import (
  DB_CONN,
  ColumnRenames,
  year_from_fiscal,
  maybe_reset,
  get_max_fiscal_time,
  filter_older_data,
)
from args import args

maybe_reset(args)


# read data
df = pd.read_csv(args.csv)

# clean data
df = df.rename(columns=ColumnRenames)
df = year_from_fiscal(df)

# are we extending?
if args.extend:
  d = get_max_fiscal_time(args)
  df = filter_older_data(df, d['year'], d['month'])

# print data
# print(df)

# write to database
df.to_sql(
  args.table,
  con=DB_CONN,
  index=False,
  if_exists='append',
)