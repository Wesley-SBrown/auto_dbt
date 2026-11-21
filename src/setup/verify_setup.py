# src/setup/verify_setup.py

import os
from dotenv import load_dotenv

from ..utils import get_connection

load_dotenv()


def verify_setup() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    warehouse = os.getenv("WAREHOUSE_NAME")
    db = os.getenv("DATABASE_NAME")
    schema = os.getenv("SCHEMA")

    try:
        # Check for warehouse
        cursor.execute(f"USE WAREHOUSE {warehouse}")
        cursor.execute(f"SHOW WAREHOUSES LIKE '{warehouse}'")
        wh_rows = cursor.fetchall()
        print(f"Warehouse '{warehouse}' found: {len(wh_rows) > 0}")
        for row in wh_rows:
            print(f"   name={row[0]}, state={row[1]}, size={row[3]}")

        # Check for database
        cursor.execute(f"SHOW DATABASES LIKE '{db}'")
        db_rows = cursor.fetchall()
        print(f"Database '{db}' found: {len(db_rows) > 0}")

        # Check schema within db
        cursor.execute(f"USE DATABASE {db}")
        cursor.execute(f"SHOW SCHEMAS LIKE '{schema}' IN DATABASE {db}")
        schema_rows = cursor.fetchall()
        print(f"Schema '{schema}' found: {len(schema_rows) > 0}")

        # Check file formats used in schema
        cursor.execute(f"USE SCHEMA {db}.{schema}")
        cursor.execute(f"SHOW FILE FORMATS IN SCHEMA {db}.{schema}")
        format_rows = cursor.fetchall()
        print(f"File formats ({len(format_rows)})")
        for row in format_rows:
            print(f"   name={row[1]}, type={row[3]}")

        # Check stages in schema
        cursor.execute(f"SHOW STAGES IN SCHEMA {db}.{schema}")
        stage_rows = cursor.fetchall()
        print(f"Stages ({len(stage_rows)})")
        for row in stage_rows:
            print(f"   name={row[1]}, type={row[3]}")

        # Check tables & cols in schema
        cursor.execute(f"SHOW TABLES IN SCHEMA {db}.{schema}")
        table_rows = cursor.fetchall()
        print(f"Tables ({len(table_rows)}):")
        for row in table_rows:
            table_name = row[1]
            print(f"   table={table_name}, rows={row[7]}, bytes={row[8]}")
            cursor.execute(f"DESCRIBE TABLE {db}.{schema}.{table_name}")
            for col in cursor.fetchall():
                print(f"       col={col[0]} ({col[1]}), null={col[3]}")


    except Exception as e:
        print(f"[ERROR] Verification failed: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__=="__main__":
    verify_setup()