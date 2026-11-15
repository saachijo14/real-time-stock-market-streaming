
import asyncio
import websockets
import json

async def test_connection():
    uri = "ws://127.0.0.1:8000/ws/stocks"

    async with websockets.connect(uri) as websocket:
        print("Connected to Stock Market WebSocket!")

        while True:
            message = await websocket.recv()
            stock = json.loads(message)

            print("\nLIVE STOCK UPDATE")
            print("Symbol:", stock["symbol"])
            print("Price:", stock["price"])
            print("Volume:", stock["volume"])

asyncio.run(test_connection())
