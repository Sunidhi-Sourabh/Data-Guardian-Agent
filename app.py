from flask import Flask, render_template, send_file
import pymysql
import markdown2
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# Load advisory report
def load_advisory():
    path = "demo_assets/risk_advice_report.md"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return markdown2.markdown(f.read())
    return "<p>No advisory report found.</p>"

# Load alert log
def load_alert_log():
    path = "demo_assets/alert_log.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().splitlines()[::-1]
    return []

@app.route("/")
def dashboard():
    advisory_html = load_advisory()
    alert_log = load_alert_log()

    # Default mock mode
    mock_mode = False
    risk_counts = {"Critical": 0, "Moderate": 0, "Low": 0, "Clean": 0}
    pattern_counts = {
        "api_key=": 0,
        "no fallback": 0,
        "open access": 0,
        "missing .env": 0,
        "malformed payload": 0
    }

    try:
        if not os.getenv("TIDB_HOST") or not os.getenv("GROQ_API_KEY"):
            mock_mode = True
            # Sample mock data
            risk_counts = {"Critical": 2, "Moderate": 3, "Low": 1, "Clean": 4}
            pattern_counts = {
                "api_key=": 3,
                "no fallback": 2,
                "open access": 1,
                "missing .env": 2,
                "malformed payload": 1
            }
        else:
            conn = pymysql.connect(
                host=os.getenv("TIDB_HOST"),
                user=os.getenv("TIDB_USER"),
                password=os.getenv("TIDB_PASSWORD"),
                database=os.getenv("TIDB_DATABASE"),
                ssl={"ssl": {}},
                connect_timeout=10
            )
            cursor = conn.cursor()
            cursor.execute("SELECT content, risk_score FROM logs")
            logs = cursor.fetchall()
            cursor.close()
            conn.close()

            for content, score in logs:
                if score >= 0.8:
                    risk_counts["Critical"] += 1
                elif score >= 0.6:
                    risk_counts["Moderate"] += 1
                elif score >= 0.5:
                    risk_counts["Low"] += 1
                else:
                    risk_counts["Clean"] += 1

                for pattern in pattern_counts.keys():
                    if pattern.lower() in content.lower():
                        pattern_counts[pattern] += 1
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        mock_mode = True

    return render_template(
        "dashboard.html",
        advisory=advisory_html,
        alerts=alert_log,
        mock_mode=mock_mode,
        risk_counts=risk_counts,
        pattern_counts=pattern_counts
    )

@app.route("/download")
def download_report():
    return send_file("demo_assets/risk_advice_report.md", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
