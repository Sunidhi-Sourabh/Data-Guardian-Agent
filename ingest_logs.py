import pymysql
from dotenv import load_dotenv
import os
from datetime import datetime

# 🔍 Check if .env exists
env_path = os.path.join(os.getcwd(), ".env")
if not os.path.isfile(env_path):
    print("⚠️ .env not found. Trying .env.txt instead...")
    env_path = os.path.join(os.getcwd(), ".env.txt")

# Load credentials from .env or .env.txt
load_dotenv(dotenv_path=env_path)

# Debug prints to verify .env loading
print("🔍 Debugging .env load:")
print("TIDB_HOST:", os.getenv("TIDB_HOST"))
print("TIDB_USER:", os.getenv("TIDB_USER"))
print("TIDB_PASSWORD:", os.getenv("TIDB_PASSWORD"))
print("TIDB_DATABASE:", os.getenv("TIDB_DATABASE"))
print("")

# Assign variables
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

# 🔧 Step 1: Connect without database to create it
print("🔗 Connecting to TiDB (no DB)...")
try:
    conn = pymysql.connect(
        host=TIDB_HOST,
        user=TIDB_USER,
        password=TIDB_PASSWORD,
        ssl={"ssl": {}},
        connect_timeout=10
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {TIDB_DATABASE}")
    print(f"✅ Database '{TIDB_DATABASE}' created or already exists.")
    cursor.close()
    conn.close()
except pymysql.MySQLError as err:
    print(f"❌ Failed to create database: {err}")
    exit(1)

# 🔁 Step 2: Reconnect to the target database
print(f"🔗 Connecting to TiDB → database: {TIDB_DATABASE}")
try:
    conn = pymysql.connect(
        host=TIDB_HOST,
        user=TIDB_USER,
        password=TIDB_PASSWORD,
        database=TIDB_DATABASE,
        ssl={"ssl": {}},
        connect_timeout=10
    )
    print("✅ Connection established.")
    cursor = conn.cursor()
except pymysql.MySQLError as err:
    print(f"❌ Connection failed: {err}")
    exit(1)

# Ensure logs table exists
try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            content TEXT,
            timestamp DATETIME,
            risk_score FLOAT
        )
    """)
    print("📦 Table 'logs' verified.")
except pymysql.MySQLError as err:
    print(f"❌ Failed to verify/create table: {err}")
    conn.close()
    exit(1)

# Insert logs into TiDB
print("📥 Inserting logs...")
for log in sample_logs:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    risk_score = 0.0  # Placeholder; will be updated by search module
    try:
        cursor.execute(
            "INSERT INTO logs (content, timestamp, risk_score) VALUES (%s, %s, %s)",
            (log, timestamp, risk_score)
        )
        print(f"📝 Inserted log: '{log}' at {timestamp}")
    except pymysql.MySQLError as err:
        print(f"❌ Failed to insert log: {log} → {err}")

conn.commit()
cursor.close()
conn.close()

print("✅ Logs ingested into TiDB successfully.")
