
import yfinance
import pandas
import confluent_kafka
import fastapi
import sqlalchemy

print("Python environment is ready!")

print("yfinance:", yfinance.__version__)
print("pandas:", pandas.__version__)
print("Kafka library:", confluent_kafka.__version__)
print("FastAPI:", fastapi.__version__)
print("SQLAlchemy:", sqlalchemy.__version__)

print("All required libraries imported successfully!")
