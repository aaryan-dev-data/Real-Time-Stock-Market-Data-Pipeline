# Real-Time Stock Market Data Pipeline (GCP | Python | PySpark | Dataflow | BigQuery)

This project fetches live stock market data from **Alpha Vantage API**, publishes it to **Google Pub/Sub**, processes it using **Dataflow (PySpark)**, and stores the results in **BigQuery** for analytics and visualization in **Looker Studio**.

---

## Architecture
1. **Alpha Vantage API** → Stock data source
2. **Cloud Run Producer (Flask + Docker)** → Publishes stock prices to Pub/Sub
3. **Pub/Sub** → Messaging layer
4. **Dataflow (PySpark)** → Processes streaming data and generates ML-ready features
5. **BigQuery** → Stores processed data
6. **Looker Studio** → Real-time visualization

<img width="787" height="113" alt="image" src="https://github.com/user-attachments/assets/aff34033-5b15-4e98-8a5c-b3a9829ef16d" />


---

## Folder Structure
- `producer/` → Cloud Run producer code
- `processor/` → PySpark Dataflow job
- `sample_data/` → Example stock messages for local testing

---

## How to Run
1. Deploy `producer/` to **Cloud Run** (Docker required).
2. Deploy `processor/` to **Dataflow**.
3. Query processed results in **BigQuery**.
4. Build dashboard in **Looker Studio**.

---
