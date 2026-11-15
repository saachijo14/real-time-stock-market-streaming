from fastapi import WebSocket, WebSocketDisconnect
from confluent_kafka import Consumer
import asyncio
import uuid
import json
from fastapi import FastAPI, HTTPException
from backend.database import get_connection
from psycopg2.extras import RealDictCursor

app = FastAPI(title="Stock Market Streaming API")

@app.get("/")
def home():
    return {"message": "Stock Market API is running!"}


# Get all stock records
@app.get("/stocks")
def get_all_stocks():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT * FROM stock_data
        ORDER BY timestamp DESC
        LIMIT 100
    """)

    records = cursor.fetchall()
    cursor.close()
    conn.close()

    return records


# Get latest price of a particular stock
@app.get("/stocks/{symbol}/latest")
def get_latest_stock(symbol: str):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT * FROM stock_data
        WHERE symbol = %s
        ORDER BY timestamp DESC
        LIMIT 1
    """, (symbol.upper(),))

    record = cursor.fetchone()
    cursor.close()
    conn.close()

    if not record:
        raise HTTPException(status_code=404, detail="Stock not found")

    return record


# Get historical stock records
@app.get("/stocks/{symbol}/history")
def get_stock_history(symbol: str):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT * FROM stock_data
        WHERE symbol = %s
        ORDER BY timestamp DESC
        LIMIT 100
    """, (symbol.upper(),))

    records = cursor.fetchall()
    cursor.close()
    conn.close()

    return records



@app.websocket("/ws/stocks")
async def stock_websocket(websocket: WebSocket):
    await websocket.accept()

    consumer = Consumer({
        "bootstrap.servers": "localhost:9092",
        "group.id": f"websocket-{uuid.uuid4()}",
        "auto.offset.reset": "latest",
        "enable.auto.commit": True
    })

    consumer.subscribe(["stock-prices"])

    print("WebSocket client connected!")

    try:
        while True:
            msg = await asyncio.to_thread(consumer.poll, 1.0)

            if msg is None:
                continue

            if msg.error():
                continue

            stock = json.loads(msg.value().decode("utf-8"))

            await websocket.send_json(stock)

    except WebSocketDisconnect:
        print("WebSocket client disconnected.")

    finally:
        consumer.close()
