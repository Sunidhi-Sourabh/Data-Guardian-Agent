"""
Ingests sample logs into TiDB Serverless for credential hygiene analysis.
Each log is stored with a timestamp and placeholder risk score.
"""

import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime

# Load credentials from .env
load_dotenv()
TIDB_HOST = os.getenv("TIDB_HOST")
TIDB_USER = os.getenv("TIDB_USER")
TIDB_PASSWORD = os.getenv("TIDB_PASSWORD")
TIDB_DATABASE = os.getenv("TIDB_DATABASE")

# Sample logs to ingest
sample_logs = [
    "api_key=12345EXPOSED",
    "User login failed: no fallback configured",
    "Access granted without token validation",
    "Missing .env discipline in deployment",
    "Secure endpoint hit with malformed payload"
]

# Connect to TiDB
conn = mysql.connector.connect(
    host=TIDB_HOST,
    user=TIDB_USER,
    password=TIDB_PASSWORD,
    database=TIDB_DATABASE,
    ssl_verify_cert=False
)
cursor = conn.cursor()

# Insert logs into TiDB
for log in sample_logs:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    risk_score = 0.0  # Placeholder; will be updated by search module
    cursor.execute(
        "INSERT INTO logs (content, timestamp, risk_score) VALUES (%s, %s, %s)",
        (log, timestamp, risk_score)
    )

conn.commit()
cursor.close()
conn.close()

print("✅ Logs ingested into TiDB successfully.")
