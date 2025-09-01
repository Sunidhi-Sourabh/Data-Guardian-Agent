import subprocess

print("🚀 Running DataGuardian Agent Pipeline...\n")

steps = [
    ("Ingesting logs", "ingest_logs.py"),
    ("Scoring risks", "search_risks.py"),
    ("Summarizing risks", "summarize_risks.py"),
    ("Triggering alert", "trigger_alert.py --mode local")
]

for label, command in steps:
    print(f"🔧 {label}...")
    result = subprocess.run(f"python {command}", shell=True)
    if result.returncode != 0:
        print(f"❌ Step failed: {label}")
        break
else:
    print("✅ Pipeline completed successfully.")
