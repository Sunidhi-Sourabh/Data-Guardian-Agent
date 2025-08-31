import mysql.connector
from dotenv import load_dotenv
import os

# Load credentials
load_dotenv()
TIDB_HOST = os.getenv("TIDB_HOST")
TIDB_USER = os.getenv("TIDB_USER")
TIDB_PASSWORD = os.getenv("TIDB_PASSWORD")
TIDB_DATABASE = os.getenv("TIDB_DATABASE")

# Risk patterns and scores
risk_patterns = {
    "api_key=": 0.9,
    "no fallback": 0.7,
    "open access": 0.8,
    "missing .env": 0.6,
    "malformed payload": 0.5
}

# Connect to TiDB
conn = mysql.connector.connect(
    host=TIDB_HOST,
    user=TIDB_USER,
    password=TIDB_PASSWORD,
    database=TIDB_DATABASE,
    ssl_verify_cert=False
)
cursor = conn.cursor()

# Fetch all logs
cursor.execute("SELECT id, content FROM logs")
logs = cursor.fetchall()

# Scan and update risk scores
for log_id, content in logs:
    score = 0.0
    for pattern, risk in risk_patterns.items():
        if pattern.lower() in content.lower():
            score = max(score, risk)
    if score > 0.0:
        cursor.execute(
            "UPDATE logs SET risk_score = %s WHERE id = %s",
            (score, log_id)
        )
        print(f"⚠️ Risk detected in log {log_id}: '{content}' → Score: {score}")

conn.commit()
cursor.close()
conn.close()

print("✅ Risk scanning completed.")
