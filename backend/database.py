
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_data (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(30) NOT NULL,
            price DECIMAL(15, 2) NOT NULL,
            volume BIGINT,
            timestamp TIMESTAMPTZ,
            fetched_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        DELETE FROM stock_data
        WHERE id IN (
            SELECT id FROM (
                SELECT id,
                       ROW_NUMBER() OVER (
                           PARTITION BY symbol, timestamp
                           ORDER BY id DESC
                       ) AS row_num
                FROM stock_data
                WHERE timestamp IS NOT NULL
            ) duplicates
            WHERE row_num > 1
        )
    """)

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS
        unique_stock_timestamp
        ON stock_data (symbol, timestamp)
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("Stock table created successfully!")


def insert_stock(stock):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO stock_data
            (symbol, price, volume, timestamp)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (symbol, timestamp)
            DO UPDATE SET
                price = EXCLUDED.price,
                volume = EXCLUDED.volume,
                fetched_at = CURRENT_TIMESTAMP
        """, (
            stock["symbol"],
            stock["price"],
            stock.get("volume"),
            stock.get("timestamp")
        ))

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()
