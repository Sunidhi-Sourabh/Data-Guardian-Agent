from flask import Flask, render_template, send_file
import pymysql
import markdown2
import os

app = Flask(__name__)

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
    return render_template("dashboard.html", advisory=advisory_html, alerts=alert_log)

@app.route("/download")
def download_report():
    return send_file("demo_assets/risk_advice_report.md", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
