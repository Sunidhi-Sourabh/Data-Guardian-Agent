import mysql.connector
from dotenv import load_dotenv
import os
import requests

# Load credentials
load_dotenv()
TIDB_HOST = os.getenv("TIDB_HOST")
TIDB_USER = os.getenv("TIDB_USER")
TIDB_PASSWORD = os.getenv("TIDB_PASSWORD")
TIDB_DATABASE = os.getenv("TIDB_DATABASE")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Connect to TiDB
conn = mysql.connector.connect(
    host=TIDB_HOST,
    user=TIDB_USER,
    password=TIDB_PASSWORD,
    database=TIDB_DATABASE,
    ssl_verify_cert=False
)
cursor = conn.cursor()

# Fetch high-risk logs
cursor.execute("SELECT content, risk_score FROM logs WHERE risk_score >= 0.5")
logs = cursor.fetchall()
cursor.close()
conn.close()

if not logs:
    print("✅ No high-risk logs found. Agent is clean.")
    exit()

# Tag severity and prepare summary
tagged_logs = []
for content, score in logs:
    if score >= 0.8:
        severity = "🔴 Critical"
    elif score >= 0.6:
        severity = "🟠 Moderate"
    else:
        severity = "🟢 Low"
    tagged_logs.append(f"{severity} → {content}")

log_summary = "\n".join(tagged_logs)

# GPT-OSS prompt
prompt = f"""
You are a privacy-first agent hygiene advisor. Analyze the following logs for credential leaks, fallback gaps, and hygiene issues. Suggest recovery steps like .env discipline, fallback logic, or credential scrub.

Logs:
{log_summary}
"""

# Call GPT-OSS via Groq
response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
)

advice = response.json()["choices"][0]["message"]["content"]
print("🧠 GPT-OSS Summary & Recommendations:\n")
print(advice)

# Export to report
with open("demo_assets/risk_advice_report.md", "w", encoding="utf-8") as file:
    file.write("# 🧠 DataGuardian Agent – Risk Summary\n\n")
    file.write("## 🔍 Tagged Logs\n")
    file.write(log_summary + "\n\n")
    file.write("## 🛠️ Recommendations\n")
    file.write(advice + "\n")

print("📄 Report saved to demo_assets/risk_advice_report.md")
