# 🛡️ DataGuardian Agent  
**Privacy-first hygiene sentinel for indie builders**  
Built for the TiDB AgentX Hackathon by [Sunidhi Sourabh]

---

## 📦 Overview  
DataGuardian Agent is a multi-step Python agent that detects credential leaks, fallback gaps, and hygiene violations in developer logs. It ingests logs into TiDB Serverless, scans for risky patterns, summarizes issues via GPT-OSS, and triggers alerts with branded fallback logic.

---

## 🧠 Features  
- 🔍 Risk Detection: Flags exposed keys, missing fallbacks, insecure access  
- 🧠 LLM Summarization: Advises recovery steps using GPT-OSS via Groq  
- 📢 Alert Triggering: Sends advisory reports via webhook or CLI  
- 🔁 Fallback Messaging: Handles GPT/DB failures with branded clarity  
- 🧾 Audit Logging: Tracks alert status and fallback events  
- 🧪 Modular CLI Flow: Each step is independently testable and cinematic

---

## 🧱 Architecture  
ingest_logs.py     → Ingest logs into TiDB
search_risks.py    → Detect hygiene risks and assign scores
summarize_risks.py → Summarize issues and suggest fixes via GPT-OSS
trigger_alert.py   → Push advisory report via webhook or CLI
fallback.py        → Provide branded fallback messages and log events

---

## ⚙️ Setup Instructions

### 1. Clone the Repo  
git clone https://github.com/sunidhisourabh/DataGuardian-Agent.git
cd DataGuardian-Agent

## 2. Create .env from Template
cp .env.template .env

  Fill in your credentials:
GROQ_API_KEY=your_key_here  
TIDB_HOST=https://your_tidb_endpoint  
TIDB_USER=your_tidb_user  
TIDB_PASSWORD=your_tidb_password  
TIDB_DATABASE=data_guardian  
WEBHOOK_URL=https://your_webhook_url

## 3. Install Dependencies
pip install -r requirements.txt

##  Run the Pipeline
python ingest_logs.py  
python search_risks.py  
python summarize_risks.py  
python trigger_alert.py --mode webhook

---

##🧾 Requirements
- Python 3.8+
- TiDB Serverless account
- Groq API key for GPT-OSS
- Webhook endpoint (Slack, Discord, etc.)

---

##📜 License
This project is licensed under the MIT License.

---

##🙌 Acknowledgments
Built for the TiDB AgentX Hackathon. Powered by TiDB Serverless, Groq GPT-OSS, and indie-grade resilience.

---

##💡 Author
Sunidhi Sourabh
Student founder, full-stack developer, and indie agent architect
Focused on privacy-first workflows, cinematic demos, and credential hygiene

🔗 Connect :-
- [Devpost]: (https://devpost.com/sunidhi-sourabh)
-[Discord]: (https://discord.gg/KBstZbht) 
[Telegram]: (https://t.me/OneStackAI)  

---

## © Copyright & Usage

All code, assets, and documentation in this repository are © 2025 Sunidhi Sourabh unless otherwise noted.

You are free to use, modify, and distribute this project under the terms of the MIT License.  
Please retain attribution and respect the privacy-first ethos of this agent when adapting or extending it.

For inquiries or collaborations, reach out via GitHub or associated contact channels.
