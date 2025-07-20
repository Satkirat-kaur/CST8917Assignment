# StoreMetadataActivity/__init__.py
import logging
import os
import pyodbc

def main(metadata: dict) -> dict:
    logging.info(f"Storing metadata: {metadata}")

    # Fetch connection string from environment variable
    conn_str = os.getenv("SQLConnectionString")
    if not conn_str:
        logging.error("Missing SQLConnectionString in environment variables.")
        return metadata

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO ImageMetadata (FileName, FileSizeKB, Width, Height, Format)
            VALUES (?, ?, ?, ?, ?)
        """

        cursor.execute(
            insert_query,
            metadata["name"],
            metadata["size_kb"],
            metadata["width"],
            metadata["height"],
            metadata["format"]
        )

        conn.commit()
        cursor.close()
        conn.close()

        logging.info("Metadata stored successfully in Azure SQL.")

    except Exception as e:
        logging.error(f"Error storing metadata in SQL: {e}")

    return metadata
