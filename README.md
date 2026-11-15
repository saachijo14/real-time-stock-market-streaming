# 📈 StockStream – Real-Time Stock Market Data Streaming Application

StockStream is a full-stack stock market data streaming application that collects stock market data, processes it through Apache Kafka, stores it in PostgreSQL, and displays stock prices through an interactive React dashboard.

The application demonstrates real-time-style data streaming using a producer-consumer architecture, REST APIs, and WebSocket communication.

## 🚀 Features

- **Stock Data Collection:** Fetches stock market data using Yahoo Finance.
- **Apache Kafka Integration:** Streams stock data through a Kafka topic.
- **Kafka Consumer:** Consumes stock messages and stores them in PostgreSQL.
- **PostgreSQL Database:** Stores stock prices, volume, and timestamps.
- **Duplicate Prevention:** Uses unique constraints and UPSERT operations to prevent duplicate stock records.
- **FastAPI Backend:** Provides REST APIs to retrieve stock information.
- **WebSocket Streaming:** Sends stock updates to connected clients.
- **React Dashboard:** Displays stock prices, trading volume, and price movement charts.
- **Automatic Reconnection:** Reconnects the dashboard when the WebSocket connection drops.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data collection and processing |
| Apache Kafka | Data streaming |
| PostgreSQL | Database |
| FastAPI | Backend REST API |
| WebSockets | Live update communication |
| React.js | Frontend dashboard |
| Vite | Frontend development |
| Recharts | Stock price visualization |
| Docker | Running Kafka and PostgreSQL |
| Yahoo Finance (`yfinance`) | Stock market data source |

## 🏗️ System Architecture

```text
             Yahoo Finance
                   |
                   v
          Python Stock Producer
                   |
                   v
             Apache Kafka
            (stock-prices)
                   |
                   v
          Python Kafka Consumer
                   |
                   v
              PostgreSQL
                   |
                   v
              FastAPI
                   |
             WebSocket
                   |
                   v
            React Dashboard
                   |
                   v
          Stock Price Charts
```

## 📊 Stocks Tracked

The application currently tracks three Indian stock market companies:

- Reliance Industries – `RELIANCE.NS`
- Tata Consultancy Services – `TCS.NS`
- Infosys – `INFY.NS`

## 📁 Project Structure

```text
stock-market-streaming/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   └── database.py
│
├── producer/
│   └── producer.py
│
├── consumer/
│   └── consumer.py
│
├── config/
│   └── settings.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   └── package.json
│
├── setup_db.py
├── test_websocket.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/saachijo14/real-time-stock-market-streaming.git
cd stock-market-streaming
```

### 2. Create a Python Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
pip install websockets python-dotenv
```

### 4. Start Kafka Using Docker

```bash
docker run -d --name kafka -p 9092:9092 apache/kafka:4.4.0
```

Create the Kafka topic:

```bash
docker exec kafka /opt/kafka/bin/kafka-topics.sh --create --topic stock-prices --bootstrap-server localhost:9092
```

### 5. Start PostgreSQL Using Docker

```bash
docker run -d --name stock-postgres -e POSTGRES_USER=stockuser -e POSTGRES_PASSWORD=stockpass123 -e POSTGRES_DB=stock_market -p 5432:5432 postgres:17
```

### 6. Configure Environment Variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_NAME=stock_market
DB_USER=stockuser
DB_PASSWORD=your_database_password
DB_PORT=5432
```

Use the same password configured for your PostgreSQL container.

### 7. Initialize the Database

```bash
python setup_db.py
```

## ▶️ Running the Application

Run each component in a separate terminal from the project root.

**Terminal 1 – FastAPI Backend**

```bash
uvicorn backend.main:app --reload
```

API documentation:

`http://127.0.0.1:8000/docs`

**Terminal 2 – Kafka Consumer**

```bash
python -m consumer.consumer
```

**Terminal 3 – Stock Data Producer**

```bash
python producer/producer.py
```

**Terminal 4 – React Frontend**

```bash
cd frontend
npm install
npm install recharts lucide-react
npm run dev
```

Open the dashboard:

`http://localhost:5173`

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API health check |
| GET | `/stocks` | Retrieve stock records |
| GET | `/stocks/{symbol}/latest` | Retrieve latest stock data |
| GET | `/stocks/{symbol}/history` | Retrieve stock price history |
| WebSocket | `/ws/stocks` | Receive stock updates |

## 🧪 Testing

The following components have been tested:

- Kafka topic creation and message streaming.
- Python producer publishing stock messages.
- Python consumer receiving messages.
- PostgreSQL database connectivity and record storage.
- Duplicate record prevention.
- FastAPI endpoints returning successful responses.
- WebSocket connection and stock updates.
- React dashboard displaying stock data and charts.
- WebSocket automatic reconnection.

## 🔮 Future Enhancements

- Add more Indian stock market symbols.
- Implement advanced stock analytics.
- Add authentication and user watchlists.
- Improve error handling and monitoring.
- Deploy the complete application to cloud infrastructure.

## ⚠️ Data Disclaimer

Stock data is fetched using Yahoo Finance through the `yfinance` library. Data availability, update frequency, and delays depend on the data provider. This application is an educational project and is not intended for financial trading decisions.

## 👩‍💻 Author

**Saachi Joshi**

Built as a project to explore real-time data streaming, distributed systems, backend development, and full-stack application development.

---

⭐ If you find this project interesting, feel free to explore the repository!