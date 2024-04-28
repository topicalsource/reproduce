import argparse

parser = argparse.ArgumentParser(description="script inputs")
parser.add_argument('--csv', help="csv file to load into database")
parser.add_argument('--table', help="SQL table to work on")
parser.add_argument('--extend', action='store_true', help="extend data in table")
parser.add_argument('--reset', action='store_true', help="reset the table before loading")

args = parser.parse_args()