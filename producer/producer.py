
import yfinance as yf
from confluent_kafka import Producer
import json
import time
from datetime import datetime, timezone

# Connect to Kafka
producer = Producer({
    "bootstrap.servers": "localhost:9092"
})

# Indian NSE stocks
stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

def delivery_report(err, msg):
    if err:
        print("Delivery failed:", err)
    else:
        print(f"Sent {msg.key().decode()} successfully")

def fetch_stock_data():
    for symbol in stocks:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="1m")

            if data.empty:
                print(f"No data available for {symbol}")
                continue

            latest = data.iloc[-1]

            message = {
                "symbol": symbol,
                "price": float(latest["Close"]),
                "volume": int(latest["Volume"]),
                "timestamp": data.index[-1].isoformat(),
                "fetched_at": datetime.now(timezone.utc).isoformat()
            }

            producer.produce(
                topic="stock-prices",
                key=symbol,
                value=json.dumps(message),
                callback=delivery_report
            )

            producer.poll(0)

        except Exception as e:
            print(f"Error fetching {symbol}: {e}")

    producer.flush()

# Continuously fetch stock data
try:
    while True:
        print("\nFetching stock prices...")
        fetch_stock_data()
        print("Waiting 60 seconds...")
        time.sleep(60)

except KeyboardInterrupt:
    print("\nProducer stopped.")
    producer.flush()
