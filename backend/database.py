import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="stock_market",
        user="stockuser",
        password="stockpass123",
        port="5432"
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

    conn.commit()
    cursor.close()
    conn.close()

    print("Stock table created successfully!")

def insert_stock(stock):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO stock_data
        (symbol, price, volume, timestamp)
        VALUES (%s, %s, %s, %s)
    """, (
        stock["symbol"],
        stock["price"],
        stock.get("volume"),
        stock.get("timestamp")
    ))

    conn.commit()
    cursor.close()
    conn.close()
