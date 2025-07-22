# Threat Intelligence Aggregator 🔍

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Python CLI tool that aggregates threat intelligence data from multiple sources, enriches it with AI analysis (via OpenAI), and outputs structured reports.

---

## 🚀 Features

- 🔎 **Multi-source aggregation**: Pull threat data from OTX, AbuseIPDB, VirusTotal
- 🤖 **AI enrichment**: Summarize and classify threats using GPT models
- 📤 **Output formats**: JSON, CSV, and Markdown
- ⚙️ **Robust operations**: Retry logic, rotating logs, and error handling
- 🧩 **Modular design**: Easily extend to support more threat sources

---

## 📁 Project Structure

ThreatIntelAggregator/
├── sources/ # Threat intel source implementations
│ ├── abuseipdb.py
│ ├── otx.py
│ └── virustotal.py
├── aggregator.py # Core aggregation logic
├── cli.py # Command-line interface
├── llm_analysis.py # AI threat analysis
├── output.py # Output formatting and writing
├── .env.example # API key config template
├── requirements.txt # Python dependencies
└── README.md # You're here

yaml
Copy code

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone git@github.com:tobialadetuyi/ThreatIntelAggregator.git
cd ThreatIntelAggregator
2. Create a Virtual Environment (Recommended)
bash
Copy code
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Configure API Keys
Copy .env.example to .env and add your keys:

ini
Copy code
OTX_API_KEY=your_otx_key
ABUSEIPDB_API_KEY=your_abuseipdb_key
VIRUSTOTAL_API_KEY=your_virustotal_key
OPENAI_API_KEY=your_openai_key
🧪 Usage Examples
🔹 Basic Aggregation
bash
Copy code
python cli.py --source otx abuseipdb
🔹 Full Pipeline with AI Analysis
bash
Copy code
python cli.py --source otx virustotal --output-format md
🔹 CLI Options
Option	Description	Default
--source	Space-separated intel sources	Required
--output-format	json, csv, or md	json
--llm	GPT model (gpt-3.5-turbo, gpt-4)	gpt-4
--llm-off	Disable AI analysis	False

🧩 Adding New Sources
Create a new Python file in sources/, e.g., shodan.py

Add a fetch_from_shodan() function returning a list of dicts:

python
Copy code
return [{
  "ip": "1.2.3.4",
  "threat": "Open RDP Detected",
  "source": "Shodan"
}]
Register the source in the main CLI or aggregator module.

📝 Logging
Logs are stored in threat_intel.log in structured JSON:

json
Copy code
{
  "timestamp": "2025-07-22T12:34:56",
  "level": "INFO",
  "message": "Fetched 42 records from OTX"
}
🤝 Contributing
We welcome contributions!

Fork the repo

Create a feature branch:
git checkout -b feature/amazing-feature

Commit and push your changes

Open a Pull Request

🛡️ Security Considerations
Store API keys in .env (never commit them)

Use .gitignore to exclude sensitive files

Rate-limit and validate API responses before acting on them

Logs avoid sensitive data where possible

❗ Troubleshooting
403 or Auth errors: Double-check your .env API keys.

No data returned: Verify API limits or test with fewer sources.

Environment errors: Use venv and correct Python version (>=3.8)

📄 License
This project is licensed under the MIT License.

📌 Author
Aladetuyi Oluwatobi - CyberAegis
GitHub: @tobialadetuyi
Twitter/X: @iamthobb
Project: ThreatIntelAggregator

Powered by Python, OpenAI GPT, and your passion for threat intelligence.
