# src/utils.py

from pathlib import Path

def get_output_path(output_filename: str) -> str:
    """
    Get full file path of data file

    Parameters
    ----------
    output_filename: str
        Compressed data file name

    Outputs
    -------
    output_filepath : str
        full file path
    """
    output_filepath = (Path(__file__)
                        .resolve()
                        .parents[1]
                        / "data" / "inputs" / output_filename
                      )
    return output_filepath

def get_connection():
    import os
    from dotenv import load_dotenv
    import snowflake.connector

    load_dotenv()

    conn = snowflake.connector.connect(
        account=os.getenv('ACCOUNT'),
        user=os.getenv('SNOWFLAKE_USER'),
        private_key_file=os.getenv('PRIVATE_KEY_FILE_PATH'),
        role=os.getenv('ROLE'),
        # private_key_password=os.getenv('PRIVATE_KEY_PASSWORD'), # Leave commented out for -nocrypt keys
        # Comment out below if running setup
        warehouse=os.getenv('WAREHOUSE_NAME'),
        database=os.getenv('DATABASE_NAME'),
        schema=os.getenv('SCHEMA'),
        enable_server_session_keep_alive_auto_detection=True
    )
    return conn