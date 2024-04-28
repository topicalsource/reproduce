import camelot
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

from util import DB_CONN, maybe_reset
from args import args

# local default / constant
args.table = "nationwide_apprehensions_yearly"

maybe_reset(args)

in_fn = "dl/U.S. Border Patrol Total Apprehensions (FY 1925 - FY 2020) (508).pdf"


def fill_from_pdf():
  # one page, two vert tables
  tables = camelot.read_pdf(in_fn)

  # strip headers
  t0 = tables[0].df.iloc[1:, :]
  t1 = tables[1].df.iloc[1:, :]

  # combine
  df = pd.concat([t0,t1], axis=0)

  # cleanup data
  df.columns = ['year','count']
  df.replace(',','', regex=True, inplace=True)

  # write to database
  df.to_sql(
    args.table,
    con=DB_CONN,
    index=False,
    if_exists='append',
  )


def extend_from_sql():
  print("extending")

  data = []
  engine = create_engine(DB_CONN)
  with engine.connect() as con:
    # drop data from 2020 so we can set newer data
    con.execute(text(f"DELETE FROM {args.table} WHERE year >= 2020"))

    query = """
    SELECT fiscal_year as year, SUM(encounter_count) as count
    FROM nationwide_encounters_aor
      WHERE encounter_type != "Inadmissibles"
    GROUP BY fiscal_year
    ORDER BY fiscal_year;
    """
    r = con.execute(text(query))
    ds = r.mappings().all()
    for d in ds:
      d = dict(d)
      data.append(d)

  df = pd.DataFrame(data, columns=["year", "count"])
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