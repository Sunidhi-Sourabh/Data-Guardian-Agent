from datetime import datetime

def fallback_message(reason="unknown"):
    messages = {
        "gpt_failure": "⚠️ GPT-OSS is currently unavailable. Please retry later or check your API key.",
        "db_unreachable": "🚫 TiDB Serverless could not be reached. Verify credentials and network access.",
        "no_risks_found": "✅ No hygiene risks detected. Your agent appears clean and resilient.",
        "report_missing": "📄 Advisory report not found. Run summarize_risks.py before triggering alerts.",
        "unknown": "⚠️ An unexpected issue occurred. Please check logs or rerun the agent."
    }
    return messages.get(reason, messages["unknown"])

def log_fallback(reason="unknown", log_path="demo_assets/alert_log.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = fallback_message(reason)
    entry = f"[{timestamp}] 🔁 Fallback triggered: {message}\n"
    try:
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(entry)
    except Exception as e:
        print(f"⚠️ Failed to log fallback: {e}")
    return message
