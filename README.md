# CLI Psycopg2 terminal app

This is a command-line interface (CLI) application built with Python and Psycopg2 that interacts with a PostgreSQL database. It allows you to perform various operations on your database tables.

## Prerequisites

Before using this application, make sure you have the following prerequisites installed:

- Python 3.x
- Psycopg2
- Dotenv
- Tabulate
- Postgres / PSQL installed locally for `pg_dump`

## Setup

Clone the repository and install the required dependencies:

```bash
pip3 install -r requirements.txt
```

### Environmental variables

Create a `.env` file in the project directory and add the necessary Postgres variables:

```
DB_HOST=your_host
DB_PORT=your_port
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
```

## Usage

To use the CLI application, run the postgres.py script with the desired function as the argument. Available functions are:

- `get_tables`: Fetch all tables in the database.
- `fetch_records`: Fetch records and metadata for a specific table.
- `backup_table`: Backup a specific table.

Examples:

```bash
python3 postgres.py get_tables
python3 postgres.py fetch_records table_name
python3 postgres.py backup_table table_name
```

Replace `table_name` with the actual name of the table you want to interact with.

**NOTE:** To back up a table, make sure you have `psql` and `postgres` installed locally for `pg_dump` to work properly.

**NOTE:** The fetch_records function accepts an optional limit argument to restrict the number of fetched records. You can provide the limit as an additional argument:

```bash
python3 postgres.py fetch_records table_name limit=10
```

This will fetch and display only the first 10 records from the specified table.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Liscense

This project is licensed under the GNU General Public License (GPL) version 3.
