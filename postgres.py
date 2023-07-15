from utils import get_tables, backup_table, fetch_records
import psycopg2
from dotenv import load_dotenv
import json
import sys

allowed_funcs = ['get_tables', 'fetch_records',
                 'backup_table', 'backup_all_tables']

if len(sys.argv) <= 1:
    print(f'You must pass a function argument: {", ".join(allowed_funcs)}')
    sys.exit(2)

# parse desired function (1st arg)
desired_func = sys.argv[1]
if desired_func not in allowed_funcs:
    print(
        f'Invalid function argument. Please choose one of the following: {", ".join(allowed_funcs)}.')
    sys.exit(2)

# parse optional args
target_table = None
target_limit = 9999999999
if len(sys.argv) >= 2:
    other_args = sys.argv[2:]
    print(other_args)
    for i, arg in enumerate(sys.argv):
        if 'table=' in arg:
            target_table = arg.replace('table=', '')
        if 'limit=' in arg:
            target_limit = arg.replace('limit=', '')
            target_limit = int(target_limit)

# exit with a non-zero status code if this func needs a table passed, and none was provided
needs_table_passed = ['backup_table', 'fetch_records']
table_arg_err = f"'{desired_func}' requires that you pass a table argument."
if not target_table and desired_func in needs_table_passed:
    print(table_arg_err)
    sys.exit(2)

print(f"table: '{target_table}' - limit: {target_limit}")

if desired_func == 'backup_table':
    backup_table(target_table)
elif desired_func == 'fetch_records':
    fetch_records(target_table, limit=target_limit)
elif desired_func == 'get_tables':
    get_tables()
elif desired_func == 'backup_all_tables':
    tables = get_tables()
    for table in tables:
        backup_table(table)
