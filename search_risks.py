import pymysql
from dotenv import load_dotenv
import os

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

# Assign credentials
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
print("🔗 Connecting to TiDB...")
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

# Fetch all logs
print("📥 Fetching logs from TiDB...")
try:
    cursor.execute("SELECT id, content FROM logs")
    logs = cursor.fetchall()
    print(f"📦 Total logs fetched: {len(logs)}\n")
except pymysql.MySQLError as err:
    print(f"❌ Failed to fetch logs: {err}")
    conn.close()
    exit(1)

# Scan and update risk scores
print("🧠 Scanning logs for risk patterns...")
for log_id, content in logs:
    print(f"📝 Scanning log {log_id}: '{content}'")
    score = 0.0
    matched = []
    for pattern, risk in risk_patterns.items():
        if pattern.lower() in content.lower():
            score = max(score, risk)
            matched.append(pattern)
            print(f"   🔍 Matched pattern: '{pattern}' → Risk: {risk}")
    if score > 0.0:
        try:
            cursor.execute(
                "UPDATE logs SET risk_score = %s WHERE id = %s",
                (score, log_id)
            )
            print(f"⚠️ Risk detected → Score updated to {score}\n")
        except pymysql.MySQLError as err:
            print(f"❌ Failed to update risk score for log {log_id}: {err}")
    else:
        print("✅ No risk patterns matched.\n")

conn.commit()
cursor.close()
conn.close()

print("✅ Risk scanning completed.")
