import psycopg2
import pandas as pd
from kafka import KafkaProducer
import json
import time
from datetime import datetime, timedelta

# ✅ TimescaleDB connection
conn = psycopg2.connect(
    host="localhost",
    database="windturbinedb",
    user="postgres",
    password="nitd123",
    port=5432
)

# ✅ Kafka Producer setup
producer = KafkaProducer(
    bootstrap_servers=['172.31.20.210:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC_NAME = 'winddata'
LOG_INTERVAL_SECONDS = 120  # ✅ Rotate log file every 30 seconds

# ✅ Fetch data from TimescaleDB
query = "SELECT * FROM wind_data ORDER BY date ASC;"
df = pd.read_sql(query, conn)
print(f"Fetched {len(df)} rows from TimescaleDB")

# ✅ Log file setup (saving to /iot-turbine-project/logs/)
current_log_start = datetime.now()
log_filename = f"../logs/log_{current_log_start.strftime('%Y%m%d_%H%M%S')}.csv"
df.iloc[0:0].to_csv(log_filename, index=False)
print(f"Created log file: {log_filename}")

# ✅ Stream data row by row
for index, row in df.iterrows():
    data = row.to_dict()

    # ✅ Convert timestamps to string
    for key, value in data.items():
        if isinstance(value, pd.Timestamp):
            data[key] = value.isoformat()

    # ✅ Send to Kafka
    producer.send(TOPIC_NAME, value=data)
    print(f"Sent row {index+1}/{len(df)} to Kafka Topic '{TOPIC_NAME}'")

    # ✅ Append to log file
    pd.DataFrame([data]).to_csv(log_filename, mode='a', index=False, header=False)

    # ✅ Rotate log file every 30 seconds
    if datetime.now() - current_log_start > timedelta(seconds=LOG_INTERVAL_SECONDS):
        print(f"Rotating log file after {LOG_INTERVAL_SECONDS} seconds")
        current_log_start = datetime.now()
        log_filename = f"../logs/log_{current_log_start.strftime('%Y%m%d_%H%M%S')}.csv"
        df.iloc[0:0].to_csv(log_filename, index=False)
        print(f"New log file: {log_filename}")

    # ✅ Simulate delay
    time.sleep(2)

producer.flush()
print("✅ Completed streaming all data from TimescaleDB to Kafka.")
