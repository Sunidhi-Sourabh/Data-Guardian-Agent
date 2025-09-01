import pymysql
from dotenv import load_dotenv
import os
import requests
from collections import Counter

# Load credentials
load_dotenv()
TIDB_HOST = os.getenv("TIDB_HOST")
TIDB_USER = os.getenv("TIDB_USER")
TIDB_PASSWORD = os.getenv("TIDB_PASSWORD")
TIDB_DATABASE = os.getenv("TIDB_DATABASE")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

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

# Fetch logs
print("📥 Fetching logs from TiDB...")
try:
    cursor.execute("SELECT content, risk_score FROM logs")
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
except pymysql.MySQLError as err:
    print(f"❌ Failed to fetch logs: {err}")
    exit(1)

total_logs = len(logs)
risky_logs = [log for log in logs if log[1] > 0.0]
highest_score = max([log[1] for log in logs], default=0.0)

# Pattern frequency
patterns = ["api_key=", "no fallback", "open access", "missing .env", "malformed payload"]
pattern_counter = Counter()

for content, score in risky_logs:
    for pattern in patterns:
        if pattern.lower() in content.lower():
            pattern_counter[pattern] += 1

# Summary print
print(f"📊 Total logs scanned: {total_logs}")
print(f"⚠️ Risky logs detected: {len(risky_logs)}")
print(f"🔥 Highest risk score: {highest_score}")
print("🔍 Top matched patterns:")
for pattern, count in pattern_counter.most_common():
    print(f"   - {pattern}: {count} matches")

# Prepare advisory prompt
tagged_logs = []
for content, score in risky_logs:
    if score >= 0.8:
        severity = "🔴 Critical"
    elif score >= 0.6:
        severity = "🟠 Moderate"
    else:
        severity = "🟢 Low"
    tagged_logs.append(f"{severity} → {content}")

log_summary = "\n".join(tagged_logs)

prompt = f"""
You are a privacy-first agent hygiene advisor. Analyze the following logs for credential leaks, fallback gaps, and hygiene issues. Suggest recovery steps like .env discipline, fallback logic, or credential scrub.

Logs:
{log_summary}
"""

# Call GPT-OSS via Groq
print("🧠 Requesting GPT-OSS advisory...")
response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "openai/gpt-oss-20b",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
)

# Debug response
print("🧾 Raw response from GPT-OSS:")
print(response.status_code)
print(response.text)

# Parse advisory
try:
    data = response.json()
    advice = data["choices"][0]["message"]["content"]
except (KeyError, IndexError) as err:
    print("❌ GPT-OSS response malformed or incomplete.")
    print("🧾 Full response:")
    print(response.text)
    exit(1)

# Display and export
print("🧠 GPT-OSS Summary & Recommendations:\n")
print(advice)

os.makedirs("demo_assets", exist_ok=True)
with open("demo_assets/risk_advice_report.md", "w", encoding="utf-8") as file:
    file.write("# 🧠 DataGuardian Agent – Risk Summary\n\n")
    file.write("## 🔍 Tagged Logs\n")
    file.write(log_summary + "\n\n")
    file.write("## 🛠️ Recommendations\n")
    file.write(advice + "\n")

print("📄 Report saved to demo_assets/risk_advice_report.md")
