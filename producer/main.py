from flask import Flask
import os, time, json, requests
from google.cloud import pubsub_v1
import threading

app = Flask(__name__)

# Env variables
PROJECT_ID = os.getenv("PROJECT_ID")
TOPIC_ID = os.getenv("TOPIC_ID")
API_KEY = os.getenv("ALPHA_VANTAGE_KEY")
SYMBOLS = os.getenv("SYMBOLS", "AAPL").split(",")

# Pub/Sub publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

DELAY_PER_REQUEST = max(60 / 5, 12)  # Alpha Vantage free: 5 requests/min

def fetch_and_publish():
    while True:
        for SYMBOL in SYMBOLS:
            try:
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={SYMBOL}&interval=1min&apikey={API_KEY}"
                resp = requests.get(url).json()

                if "Time Series (1min)" not in resp:
                    print(f"No data for {SYMBOL}, retrying...")
                    continue

                ts = sorted(resp["Time Series (1min)"].keys())[-1]
                data = resp["Time Series (1min)"][ts]

                message = {
                    "timestamp": ts,
                    "symbol": SYMBOL,
                    "price": float(data["1. open"]),
                    "volume": int(data["5. volume"]),
                    "open": float(data["1. open"]),
                    "high": float(data["2. high"]),
                    "low": float(data["3. low"])
                }

                publisher.publish(topic_path, json.dumps(message).encode("utf-8"))
                print(f"Published: {message}")

            except Exception as e:
                print(f"Error fetching {SYMBOL}: {e}")

            time.sleep(DELAY_PER_REQUEST)

@app.route("/")
def index():
    return "Stock producer running!"

if __name__ == "__main__":
    threading.Thread(target=fetch_and_publish).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
