from utils import get_tables, backup_table, fetch_records, grep_sql_files, fetch_table_constraints
from utils import fetch_latest_records, fetch_table_schema, get_table_size, query_table, nearby_records
from utils import nearby_records, get_indexes

import psycopg2
from dotenv import load_dotenv
import json
import sys

allowed_funcs = ['tables', 'fetch', 'constraints', 'latest', 'nearby', 'indexes',
                 'backup', 'backup', 'search', 'schema', 'size', 'query']

if len(sys.argv) <= 1:
    print(f'You must pass a function argument: {", ".join(allowed_funcs)}')
    sys.exit(2)

# parse desired function (1st arg)
desired_func = sys.argv[1]
if desired_func not in allowed_funcs:
    print(f'Invalid function argument. Please choose one of the following: {", ".join(allowed_funcs)}.')
    sys.exit(2)

# parse optional args
target_table = None
target_search = None
target_limit = 9999999999
target_lat = None
target_lng = None

if len(sys.argv) >= 2:
    other_args = sys.argv[2:]
    print(other_args)
    for i, arg in enumerate(sys.argv):
        if 'table=' in arg:
            target_table = arg.replace('table=', '')
        if 'limit=' in arg:
            target_limit = arg.replace('limit=', '')
            target_limit = int(target_limit)
        if 'search=' in arg:
            target_search = arg.replace('search=', '')
        if 'lat=' in arg:
            target_lat = arg.replace('lat=', '')
            target_lat = float(target_lat)
        if 'lng=' in arg:
            target_lng = arg.replace('lng=', '')
            target_lng = float(target_lng)

if desired_func == "nearby":
    if not target_lat or not target_lng or not target_table:
        print(f"'{desired_func}' requires that you pass 'table', 'lat', and 'lng' arguments.")
        sys.exit(2)        

# exit with a non-zero status code if this func needs a table passed, and none was provided
needs_table_passed = ['backup', 'fetch', 'constraints', 'latest', 'size', 'schema', 'query', 'nearby', 'indexes']
table_arg_err = f"'{desired_func}' requires that you pass a 'table' argument."
if not target_table and desired_func in needs_table_passed:
    print(table_arg_err)
    sys.exit(2)

# exit with a non-zero status code if this func needs a 'search' passed, and none was provided
needs_search_passed = ['search', 'query']
search_arg_err = f"'{desired_func}' requires that you pass a 'search' argument."
if desired_func in needs_search_passed and not target_search:
    print(search_arg_err)
    sys.exit(2)

print(f"table: '{target_table}' - limit: {target_limit}")

if desired_func == 'backup':
    backup_table(target_table)
elif desired_func == 'fetch':
    fetch_records(target_table, limit=target_limit)
elif desired_func == 'constraints':
    fetch_table_constraints(target_table)
elif desired_func == 'tables':
    get_tables()
elif desired_func == 'search':
    grep_sql_files(target_search)
elif desired_func == 'indexes':
    get_indexes(target_table)
elif desired_func == 'latest':
    fetch_latest_records(target_table, target_limit)
elif desired_func == 'schema':
    fetch_table_schema(target_table)
elif desired_func == 'size':
    get_table_size(target_table)
elif desired_func == 'query':
    query_table(target_table, target_search, target_limit)
elif desired_func == 'nearby':
    nearby_records(target_table, target_lat, target_lng)
elif desired_func == 'backup_all':
    tables = get_tables()
    for table in tables:
        backup_table(table)
