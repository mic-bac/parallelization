"""
db_rw_optional.py
-----------------
Demonstration: Write a CSV file to a PostgreSQL database and read it back using Python.

This script is designed for teaching purposes and shows how to:
- Connect to a PostgreSQL database using SQLAlchemy
- Write a pandas DataFrame to the database
- Read data back from the database into pandas

Requirements:
- psycopg2 (or psycopg2-binary)
- pandas
- SQLAlchemy

Make sure your PostgreSQL container is running and accessible.
"""

# %%
import pandas as pd
from sqlalchemy import create_engine

# %%
# --- 1. Define database connection parameters ---
DB_USER = 'myuser'                 # Database username
DB_PASS = 'mypassword'             # Database password
DB_HOST = 'localhost'              # Hostname (use 'localhost' or '127.0.0.1')
DB_PORT = '5432'                   # Default PostgreSQL port
DB_NAME = 'mydatabase'             # Database name
TABLE_NAME = 'parallel_big_data'   # Table to write/read

# %%
# --- 2. Create a SQLAlchemy engine (connection object) ---
# The engine manages connections to the database.
engine = create_engine(
    f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

# %%
# --- 3. Load the CSV file into a pandas DataFrame ---
print('Reading parallel_big_data.csv into pandas DataFrame...')
df = pd.read_csv('parallel_big_data.csv')
print(f'DataFrame loaded with shape: {df.shape}')

# %%
# --- 4. Write the DataFrame to PostgreSQL ---
print(f'Writing DataFrame to PostgreSQL table "{TABLE_NAME}" (this may take a while)...')
df.to_sql(
    TABLE_NAME,
    engine,
    if_exists='replace',  # Overwrite table if it exists
    index=False,          # Don't write DataFrame index as a column
    method='multi',       # Use multi-row insert for speed
    chunksize=10000       # Write in chunks of 10,000 rows
)
print(f'Data written to table "{TABLE_NAME}".')

# %%
# --- 5. Read the data back from PostgreSQL into a new DataFrame ---
print(f'Reading data back from table "{TABLE_NAME}"...')
df_db = pd.read_sql(f'SELECT * FROM {TABLE_NAME}', engine)
print(f'Read {len(df_db)} rows from table "{TABLE_NAME}".')

# %%
# --- 6. Optional: Show a sample of the loaded data ---
print('Sample of data loaded from the database:')
print(df_db.head())

# %%
# --- 7. Optional: Show data types of the DataFrame ---
print('Data types of the original DataFrame:')
print(df.dtypes)
print('Data types of the DataFrame read from the database:')
print(df_db.dtypes)
# %%
