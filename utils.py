import sys
import os
import subprocess
import json
import datetime

# Custom JSON encoder to handle datetime objects


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        return super().default(o)


def install_required_packages():
    print("Required packages are missing. Would you like to install them? (y/n)")

    user_input = input().lower()
    if user_input == 'y':
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "tabulate", "psycopg2"])
            print("Packages installed successfully.")
        except subprocess.CalledProcessError:
            print("Failed to install packages.")
    else:
        print("Aborted package installation.")


try:
    from dotenv import load_dotenv
    import psycopg2
    from tabulate import tabulate
except ImportError as e:
    print("Failed to import required packages.")
    install_required_packages()
    sys.exit(1)


def handle_errors(err):
    """
    Pretty print and colorize error messages
    """

    if isinstance(err, (AttributeError, psycopg2.OperationalError)):
        print("\x1b[31mError: Failed to connect to the database.\x1b[37m")
        print("\x1b[33mPlease ensure that the PostgreSQL server is running, and the environment variables (in .env) are correct.\x1b[37m")
    else:
        exception_type = type(err).__name__
        error_message = str(err)
        line_number = sys.exc_info()[-1].tb_lineno
        print(
            f"\x1b[31m{exception_type} at line {line_number} - {error_message}\x1b[37m")


def connect():
    """
    Connect to the Postgres database using psycopg2
    """

    try:

        # Load environment variables from .env file
        load_dotenv()

        # Access environment variables
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )

        return conn
    except Exception as err:
        handle_errors(err)


def grep_sql_files(search_string):
    sql_files = [file for file in os.listdir('.') if file.endswith('.sql')]

    for file_name in sql_files:
        with open(file_name, 'r') as file:
            lines = file.read().splitlines()
            print_line = False
            for line in lines:
                if search_string in line:
                    print('\n')
                    print_line = True

                if print_line:
                    print(line)

                if ';' in line:
                    print_line = False


def backup_table(table):
    """
    Use pg_dump to backup a table
    """

    try:
        backup_file = f'{table}.backup.sql'
        # green
        print(
            f"\n\x1b[32mCreating backup for '{table}' to {backup_file}\x1b[37m")

        # Load environment variables from .env file
        load_dotenv()

        # Access environment variables
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')

        # Set the PGPASSWORD environment variable
        os.environ['PGPASSWORD'] = db_password

        command = f'pg_dump -h {db_host} -p {db_port} -U {db_user} -d {db_name} --table={table}'
        with open(backup_file, 'w') as f:
            subprocess.run(command, shell=True, stdout=f)
    except Exception as err:
        handle_errors(err)

    sys.stdout.write('\a')
    sys.stdout.flush()


def fetch_records(table, limit=None):
    """
    Fetch records and metadata for a Postgres table
    """

    conn = connect()
    cursor = conn.cursor()

    try:
        query = f"SELECT * FROM {table}"
        if limit is not None and limit > 0:
            query += f" LIMIT {int(limit)}"

        cursor.execute(query)
        rows = cursor.fetchall()

        # Collect data as a list of dictionaries with column names as keys
        records_list = []
        headers = [column[0] for column in cursor.description]
        for row in rows:
            record_dict = dict(zip(headers, row))
            records_list.append(record_dict)

        # Print records as JSON using the custom encoder
        try:
            print(json.dumps(records_list, indent=4, cls=DateTimeEncoder))
        except Exception as e:
            print(e)
            # print(records_list)
            for i in range(len(records_list)):
                item = records_list[i]
                # Use the custom encoder here
                print(json.dumps(item, indent=4, cls=DateTimeEncoder))

        # Print metadata
        print('\n\x1b[32mMetadata:\x1b[37m')  # green
        for column in cursor.description:
            print(column)

        cursor.close()
        conn.close()

    except Exception as err:
        print(err)
        handle_errors(err)


def fetch_table_constraints(table):
    """
    Fetch table constraints for a Postgres table
    """

    conn = connect()
    cursor = conn.cursor()

    try:
       # Get table constraints
        query = """
            SELECT conname, pg_get_constraintdef(oid)
            FROM pg_constraint
            WHERE conrelid = (
                SELECT oid
                FROM pg_class
                WHERE relname = %s
            )
        """
        cursor.execute(query, (table,))
        rows = cursor.fetchall()

        # Collect data as a list of dictionaries with constraint names and sources as keys
        constraints_list = []
        headers = [column[0] for column in cursor.description]
        for row in rows:
            constraint_dict = dict(zip(headers, row))
            constraints_list.append(constraint_dict)

        # Print constraints as JSON using the custom encoder
        try:
            print(json.dumps(records_list, indent=4, cls=DateTimeEncoder))
        except:
            for i in range(len(constraints_list)):
                item = constraints_list[i]
                print(json.dumps(item, indent=4, cls=DateTimeEncoder))

        cursor.close()
        conn.close()

    except Exception as err:
        handle_errors(err)


def get_tables():
    """
    Get all of the tables for the database set in the .env file
    """

    conn = connect()
    cursor = conn.cursor()

    final_tables = []

    try:
        # Execute query to fetch table names
        cursor.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            """
        )
        table_names = [row[0] for row in cursor.fetchall()]

        # Print the table names
        print('\n\n\x1b[32mTable Names:\n\x1b[37m')
        for table_name in table_names:
            print(table_name)
            final_tables.append(table_name)

        cursor.close()
        conn.close()

    except Exception as err:
        handle_errors(err)

    return final_tables
