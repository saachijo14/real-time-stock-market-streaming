
import { useEffect, useState } from "react";
import {
  LineChart, Line, XAxis, YAxis,
  Tooltip, ResponsiveContainer, CartesianGrid
} from "recharts";
import {
  Activity, TrendingUp, 
  Wifi, WifiOff, RefreshCw
} from "lucide-react";
import "./App.css";

const API = "http://127.0.0.1:8000";
const WS = "ws://127.0.0.1:8000/ws/stocks";

const initialStocks = [
  { symbol: "RELIANCE.NS", name: "Reliance Industries" },
  { symbol: "TCS.NS", name: "Tata Consultancy Services" },
  { symbol: "INFY.NS", name: "Infosys" }
];

function App() {
  const [stocks, setStocks] = useState({});
  const [history, setHistory] = useState([]);
  const [selected, setSelected] = useState("RELIANCE.NS");
  const [connected, setConnected] = useState(false);
  const [loading, setLoading] = useState(true);

  // Fetch historical records
  useEffect(() => {
  let cancelled = false;

  async function loadHistory() {
    try {
      const response = await fetch(`${API}/stocks/${selected}/history`);
      if (!response.ok) throw new Error("History unavailable");

      const data = await response.json();

      if (!cancelled) {
        setHistory(data.reverse().map(item => ({
          time: new Date(item.timestamp).toLocaleTimeString(),
          price: Number(item.price)
        })));
      }
    } catch (error) {
      console.error("History error:", error);
      if (!cancelled) setHistory([]);
    } finally {
      if (!cancelled) setLoading(false);
    }
  }

  loadHistory();

  return () => {
    cancelled = true;
  };
}, [selected]);

  // Connect to Kafka updates through WebSocket
  useEffect(() => {
    const socket = new WebSocket(WS);

    socket.onopen = () => setConnected(true);
    socket.onclose = () => setConnected(false);
    socket.onerror = () => setConnected(false);

    socket.onmessage = (event) => {
      const stock = JSON.parse(event.data);

      setStocks(previous => ({
        ...previous,
        [stock.symbol]: stock
      }));

      if (stock.symbol === selected) {
        setHistory(previous => [
          ...previous,
          {
            time: new Date(
              stock.fetched_at || stock.timestamp
            ).toLocaleTimeString(),
            price: Number(stock.price)
          }
        ].slice(-50));
      }
    };

    return () => socket.close();
  }, [selected]);

  // Load latest stored records initially
  useEffect(() => {
    async function loadStocks() {
      try {
        const response = await fetch(`${API}/stocks`);
        const data = await response.json();

        const latest = {};

        data.forEach(stock => {
          if (!latest[stock.symbol]) {
            latest[stock.symbol] = stock;
          }
        });

        setStocks(previous => ({ ...latest, ...previous }));
      } catch (error) {
        console.error("Stock loading error:", error);
      }
    }

    loadStocks().finally(() => setLoading(false));
  }, []);

  const currentStock = stocks[selected];
  const chartData = history;

  return (
    <div className="dashboard">

      <header className="topbar">
        <div className="brand">
          <Activity size={27} />
          <span>StockStream</span>
        </div>

        <div className="connection">
          {connected ? (
            <>
              <Wifi size={17} />
              <span>Live Connected</span>
            </>
          ) : (
            <>
              <WifiOff size={17} />
              <span>Disconnected</span>
            </>
          )}
        </div>
      </header>

      <main className="container">

        <section className="welcome">
          <div>
            <p className="eyebrow">INDIAN STOCK MARKET</p>
            <h1>Market Overview</h1>
            <p>Track your stocks and monitor market movements.</p>
          </div>
          <div className="live-label">
            <span className="pulse"></span>
            LIVE MARKET DATA
          </div>
        </section>

        <section className="stock-grid">
          {initialStocks.map(stock => {
            const data = stocks[stock.symbol];
            const isSelected = selected === stock.symbol;

            return (
              <div
                key={stock.symbol}
                className={`stock-card ${isSelected ? "selected" : ""}`}
                onClick={() => setSelected(stock.symbol)}
              >
                <div className="card-top">
                  <div>
                    <h3>{stock.symbol.replace(".NS", "")}</h3>
                    <p>{stock.name}</p>
                  </div>
                  <TrendingUp size={22} />
                </div>

                <h2>
                  {data
                    ? `₹${Number(data.price).toLocaleString("en-IN", {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                      })}`
                    : "Waiting for data..."}
                </h2>

                <div className="card-bottom">
                  <span>Volume</span>
                  <strong>
                    {data
                      ? Number(data.volume).toLocaleString("en-IN")
                      : "--"}
                  </strong>
                </div>

                <span className="select-hint">
                  {isSelected ? "Currently selected" : "View chart →"}
                </span>
              </div>
            );
          })}
        </section>

        <section className="chart-section">
          <div className="chart-heading">
            <div>
              <p className="eyebrow">PRICE ANALYSIS</p>
              <h2>{selected.replace(".NS", "")} Price Movement</h2>
            </div>

            <div className="price-display">
              <strong>
                {currentStock
                  ? `₹${Number(currentStock.price).toFixed(2)}`
                  : "--"}
              </strong>
              <span>Latest available price</span>
            </div>
          </div>

          <div className="chart-container">
            {loading ? (
              <p>Loading chart...</p>
            ) : chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#293449" />
                  <XAxis dataKey="time" stroke="#8995aa" />
                  <YAxis
                    domain={["auto", "auto"]}
                    stroke="#8995aa"
                  />
                  <Tooltip
                    contentStyle={{
                      background: "#172033",
                      border: "1px solid #334155",
                      borderRadius: "10px"
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="price"
                    stroke="#38bdf8"
                    strokeWidth={3}
                    dot={false}
                    activeDot={{ r: 5 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <p className="empty">
                No historical data available yet.
              </p>
            )}
          </div>
        </section>

        <section className="info-footer">
          <div>
            <Activity size={20} />
            <span>Powered by Apache Kafka</span>
          </div>
          <div>
            <RefreshCw size={17} />
            <span>WebSocket streaming</span>
          </div>
        </section>

      </main>
    </div>
  );
}

export default App;
