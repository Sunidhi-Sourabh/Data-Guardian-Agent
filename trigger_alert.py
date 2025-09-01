import os
import requests
import argparse
import pymysql
from dotenv import load_dotenv
from datetime import datetime

# Load credentials
load_dotenv()
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
TIDB_HOST = os.getenv("TIDB_HOST")
TIDB_USER = os.getenv("TIDB_USER")
TIDB_PASSWORD = os.getenv("TIDB_PASSWORD")
TIDB_DATABASE = os.getenv("TIDB_DATABASE")

# CLI flags
parser = argparse.ArgumentParser(description="Trigger alert from DataGuardian Agent")
parser.add_argument("--mode", choices=["local", "webhook"], default="local", help="Choose alert mode")
args = parser.parse_args()

# Read advisory report
report_path = "demo_assets/risk_advice_report.md"
if not os.path.exists(report_path):
    print("⚠️ No advisory report found. Run summarize_risks.py first.")
    exit()

with open(report_path, "r", encoding="utf-8") as file:
    report_content = file.read()

# Optional: Verify TiDB connection before alerting
print("🔗 Verifying TiDB connection...")
try:
    conn = pymysql.connect(
        host=TIDB_HOST,
        user=TIDB_USER,
        password=TIDB_PASSWORD,
        database=TIDB_DATABASE,
        ssl={"ssl": {}},
        connect_timeout=10
    )
    conn.close()
    print("✅ TiDB connection verified.")
except pymysql.MySQLError as err:
    print(f"❌ TiDB connection failed: {err}")
    exit(1)

# Format payload for Slack/Discord markdown
formatted_payload = {
    "text": f"*🛡️ DataGuardian Agent Risk Report*\n\n```markdown\n{report_content}\n```"
}

# Trigger alert based on mode
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_entry = ""

if args.mode == "webhook":
    response = requests.post(WEBHOOK_URL, json=formatted_payload)
    if response.status_code == 200:
        print("✅ Alert sent successfully via webhook.")
        log_entry = f"[{timestamp}] ✅ Webhook alert sent.\n"
    else:
        print(f"❌ Failed to send alert. Status code: {response.status_code}")
        log_entry = f"[{timestamp}] ❌ Webhook alert failed. Status: {response.status_code}\n"
else:
    print("📢 Local Alert:\n")
    print(report_content)
    log_entry = f"[{timestamp}] 📢 Local alert displayed.\n"

# Log alert status
os.makedirs("demo_assets", exist_ok=True)
with open("demo_assets/alert_log.txt", "a", encoding="utf-8") as log_file:
    log_file.write(log_entry)
