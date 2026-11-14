
from confluent_kafka import Consumer
from backend.database import create_table, insert_stock
import json

create_table()

consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "stock-db-consumer",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False
})

consumer.subscribe(["stock-prices"])

print("Listening for stock updates...")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print("Kafka error:", msg.error())
            continue

        stock = json.loads(msg.value().decode("utf-8"))

        try:
            insert_stock(stock)
            consumer.commit(message=msg, asynchronous=False)

            print("\nStock saved to PostgreSQL!")
            print("Symbol:", stock["symbol"])
            print("Price:", stock["price"])

        except Exception as e:
            print("Database error:", e)

except KeyboardInterrupt:
    print("Consumer stopped.")

finally:
    consumer.close()
