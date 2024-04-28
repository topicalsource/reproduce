from pandas import DataFrame
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy import text

DB_CONN = "mysql+pymysql://ts:ts@localhost:3306/us-border"

def maybe_reset(args):
  if args.reset:
    print(f"reset: {args.table}")
    engine = create_engine(DB_CONN)

    with engine.connect() as con:
      try:
        con.execute(text(f"DROP TABLE {args.table};"))
      except Exception as e:
        print(e)
      with open(f"schemas/{args.table}.sql") as f:
        query = text(f.read())
        con.execute(query)


def get_max_fiscal_time(args):
  engine = create_engine(DB_CONN)
  query = f"""
  SELECT year, month
  FROM {args.table}
  GROUP BY year, month
  ORDER BY year DESC, month DESC
  LIMIT 12
  """

  with engine.connect() as con:
    r = con.execute(text(query))
    ds = r.mappings().all()
    d = ds[0]
    return {
      'year': int(d['year']),
      'month': MonthToInt[d['month']],
    }


Regions = {
  "Livermore": "Coastal",
  "Miami": "Coastal",
  "New Orleans": "Coastal",
  "Ramey": "Coastal",

  "Blaine": "Northern",
  "Boston": "Northern",
  "Buffalo": "Northern",
  "Detroit": "Northern",
  "Grand Forks": "Northern",
  "Havre": "Northern",
  "Houlton": "Northern",
  "Portland": "Northern",
  "Seattle": "Northern",
  "Spokane": "Northern",
  "Swanton": "Northern",

  "Big Bend": "Southern",
  "Del Rio": "Southern",
  "El Centro": "Southern",
  "El Paso": "Southern",
  "Laredo": "Southern",
  "Rio Grande Valley": "Southern",
  "San Diego": "Southern",
  "Tucson": "Southern",
  "Yuma": "Southern",

  "Coastal Border": "Coastal",
  "Northern Border": "Northern",
  "Southwest Border": "Southern",
}

# fiscal year
FiscalMonths = {
  1: "OCT",
  2: "NOV",
  3: "DEC",
  4: "JAN",
  5: "FEB",
  6: "MAR",
  7: "APR",
  8: "MAY",
  9: "JUN",
  10: "JUL",
  11: "AUG",
  12: "SEP",
}

FiscalMonthToInt = {
  "OCT": 1,
  "NOV": 2,
  "DEC": 3,
  "JAN": 4,
  "FEB": 5,
  "MAR": 6,
  "APR": 7,
  "MAY": 8,
  "JUN": 9,
  "JUL": 10,
  "AUG": 11,
  "SEP": 12,
}

MonthToInt = {
  "JAN": 1,
  "FEB": 2,
  "MAR": 3,
  "APR": 4,
  "MAY": 5,
  "JUN": 6,
  "JUL": 7,
  "AUG": 8,
  "SEP": 9,
  "OCT": 10,
  "NOV": 11,
  "DEC": 12,
}

ColumnRenames = {
  "Fiscal Year": "fiscal_year",
  "Month Grouping": "month_grouping",
  "Month (abbv)": "month",
  "Component": "component",
  "Demographic": "demographic",
  "Citizenship Grouping": "citizenship",
  "Title of Authority": "title_of_authority",
  "Encounter Type": "encounter_type",
  "Encounter Count": "encounter_count",
  "Land Border Region": "region",
  "Area of Responsibility": "area_of_responsibility",
  "AOR (Abbv)": "aor",
}

def year_from_fiscal(df: DataFrame) -> DataFrame:
  df["year"] = df["fiscal_year"]
  def transform_row(r):
    if type(r.fiscal_year) == str and len(r.fiscal_year) > 4:
      r.fiscal_year = r.fiscal_year[:4]
    if type(r.year) == str and len(r.year) > 4:
      r.year = r.year[:4]
    r.year = int(r.year) - 1 if r.month in ["OCT", "NOV", "DEC"] else int(r.year)
    return r
  return df.apply(transform_row, axis=1)

def add_int_month(df: DataFrame) -> DataFrame:
  def transform_row(r):
    r['imonth'] = MonthToInt[r.month]
    return r
  return df.apply(transform_row, axis=1)

def filter_older_data(df: DataFrame, year: int, month: int):
  df = add_int_month(df)
  # filter for only newer data
  df = df.loc[
    (df['year'] > year) | (
      (df['year'] == year) & (df['imonth'] > month)
    )
  ].drop('imonth', axis=1)
  # drop extra imonth helper column 
  return df