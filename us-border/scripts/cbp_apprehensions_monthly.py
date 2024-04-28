
import camelot
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

from util import (
  DB_CONN,
  FiscalMonths,
  Regions,
  filter_older_data,
  maybe_reset,
  get_max_fiscal_time,
)
from args import args


# local default / constant
args.table = "cbp_apprehensions_monthly"

maybe_reset(args)


def fill_from_pdf():
  # source
  fn = "dl/us-cbp-monthly-encounters-2000-2020.pdf"
  tables = camelot.read_pdf(fn, pages="all")

  data = []
  for page in range(0, len(tables)):
    orig = tables[page].df

    # uncomment to see sufficient data for comparing to PDF
    # print(orig)
    # print("\n\n")

    # CLEANUP
    # remove monthly total row & yearly total column
    orig = orig.iloc[:-1, :-1]
    # remove commas from numbers
    orig.replace(',','', regex=True, inplace=True)

    # reshape, loop over rows (geography)
    for _, row in orig[1:].iterrows():
      sector = row[0]
      # livermore is discontinued after a few years
      # it has an '*' at the end when it becomes n/a
      if sector == "Livermore*":
        continue
      # skip some summary rows that we can calculate in SQL
      if "Border" in sector:
        continue
      if "\n" in sector:
        sector = sector[:sector.index("\n")]
      region = Regions[sector] + " Border"

      # for each column (month)
      for c in range(1,12):
        fiscal_year = 2000+page
        # year & correction
        year = fiscal_year
        if c < 4:
          year -= 1
        d = [
          fiscal_year,
          year,
          FiscalMonths[c],
          sector,
          region,
          row[c],
        ]
        data.append(d)


  # create final dataframe
  df = pd.DataFrame(data, columns=["fiscal_year", "year", "month", "sector", "region", "count"])
  # print(df)

  # write to database
  df.to_sql(
    args.table,
    con=DB_CONN,
    index=False,
    if_exists='append',
  )

def extend_from_sql():
  print("extending")

  # get the latest time in target table
  mft = get_max_fiscal_time(args)

  engine = create_engine(DB_CONN)
  query = f"""
  SELECT fiscal_year, year, month, region as sector, area_of_responsibility as region, encounter_count as count
  FROM nationwide_encounters_aor
    WHERE encounter_type != "Inadmissibles"
      AND fiscal_year >= {mft['year']}
  """



  data = []
  with engine.connect() as con:
    # get data from SQL
    r = con.execute(text(query))
    ds = r.mappings().all()
    for d in ds:
      d = dict(d)
      # clean area of responsibility
      a = d["region"]
      if "Field Office" in a:
        a = a[:-13]
      if "Sector" in a:
        a = a[:-7]
      d["year"] = int(d["year"])
      d["region"] = a
      d["sector"] = Regions[a] + " Border"
      data.append(d)


  print(data[:9])
  print(data[-9:])
  # build dataframe of newer data
  df = pd.DataFrame(data, columns=["fiscal_year", "year", "month", "sector", "region", "count"])
  df = filter_older_data(df, mft['year'], mft['month'])
  print(df)

  # write to database
  df.to_sql(
    args.table,
    con=DB_CONN,
    index=False,
    if_exists='append',
  )

if args.extend:
  extend_from_sql()
else:
  fill_from_pdf()