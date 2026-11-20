# src/base_queries

"""
Contains base queries for interacting with Snowflake
"""

QUERIES = {
    "create_warehouse": """
        CREATE WAREHOUSE IF NOT EXISTS $warehouse_name
            WAREHOUSE_SIZE = 'XSMALL'
            AUTO_SUSPEND = 300
            AUTO_RESUME = TRUE
            INITIALLY_SUSPENDED = TRUE;
    """,
    "create_database": """
        CREATE DATABASE IF NOT EXISTS $database_name;
    """,
    "use_database": """
        USE DATABASE $database_name;
    """,
    "use_warehouse": """
        USE WAREHOUSE $warehouse_name;
    """,
    "create_schema": """
        CREATE SCHEMA IF NOT EXISTS $database_name.$schema;
    """,
    "use_schema": """
        USE SCHEMA $database_name.$schema;
    """,
    "create_jsonl_gz_format": """
        CREATE OR REPLACE FILE FORMAT jsonl_gz_format
            TYPE = 'JSON'
            COMPRESSION = 'GZIP';
    """,
    "create_landing_stage": """
        CREATE OR REPLACE STAGE raw_landing_stage
            FILE_FORMAT = jsonl_gz_format;
    """,
    "create_raw_data_table": """
        CREATE OR REPLACE TABLE raw_events (
            raw_data VARIANT,
            _source_file VARCHAR,
            _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        );
    """

}