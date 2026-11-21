# src/setup/setup.py

import os
from string import Template
from dotenv import load_dotenv

from ..utils import get_connection
from ..base_queries import QUERIES

load_dotenv()

def run_setup() -> None:
    """
    Runs pre-defined setup queries found in base_queries.py
    using user defined env vars
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Collect snowflake storage vars
    context = {
        "warehouse_name": os.getenv("WAREHOUSE_NAME"),
        "database_name": os.getenv("DATABASE_NAME"),
        "schema": os.getenv("SCHEMA")
    }

    # Setup order execution
    execution_order = [
        "create_warehouse",
        "create_database",
        "use_warehouse",
        "use_database",
        "create_schema",
        "use_schema",
        "create_jsonl_gz_format",
        "create_landing_stage",
        "create_raw_data_table"
    ]

    try:
        for query in execution_order:
            raw_query = QUERIES[query]
            # Use string.Template for vars imputation
            formatted_query = Template(raw_query).safe_substitute(context)
            
            print(f"Executing: {query}...")
            cursor.execute(formatted_query)
            
        print("Snowflake environment successfully set up!")
        
    except Exception as e:
        print(f"Error during setup: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    run_setup()