# src/load/load_raw.py

from pathlib import Path
from dotenv import load_dotenv

from ..utils import get_output_path, get_connection

load_dotenv()

def load_jsonl_to_snowflake(
    file_path: str, table_name: str, stage_name: str = "raw_landing_stage"
)-> None:
    """
    Loads raw .jsonl.gz file into snowflake and unpacks, purging the .gz file copy

    Parameters
    ----------
    file_path : str
        .gz file path location
    table_name : str
        Table to save data to
    stage_name : str
        Temp storage for .gz while being unpacked and populated into table
    """
    # Resolve absolute path and format as a POSIX URI for Snowflake's PUT command
    abs_path = Path(file_path).resolve().as_posix()
    file_name = Path(file_path).name

    conn = get_connection()

    try:
        cursor = conn.cursor()

        # Upload local .jsonl.gz to the Snowflake internal stage
        # AUTO_COMPRESS=FALSE prevents Snowflake from double-gzipping the file
        put_sql = f"""
            PUT 'file://{abs_path}' @{stage_name}
            AUTO_COMPRESS = FALSE
            OVERWRITE = TRUE
        """
        cursor.execute(put_sql)

        # Bulk load from stage into the VARIANT column
        # PURGE=TRUE automatically deletes the file from the stage after a successful load
        # NOTE: If ran again on same data, it will create duplicate entries
        copy_sql = f"""
            COPY INTO {table_name} (raw_data, _source_file)
            FROM (
                SELECT 
                    $1, 
                    METADATA$FILENAME
                FROM @{stage_name}/{file_name}
            )
            FILE_FORMAT = (FORMAT_NAME = 'jsonl_gz_format')
            PURGE = TRUE
            ON_ERROR = 'ABORT_STATEMENT'
        """
        result = cursor.execute(copy_sql).fetchall()
        print(f"Load complete: {result}")

    finally:
        conn.close()

if __name__ == "__main__":
    target_file = get_output_path("meta_Automotive.jsonl.gz")
    load_jsonl_to_snowflake(file_path=target_file, table_name="raw_events")