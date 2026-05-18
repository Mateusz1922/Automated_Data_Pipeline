# 📈 Professional Market Data ETL & Analytics Pipeline

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org)
[![Database](https://img.shields.io/badge/database-DuckDB%20%7C%20Snowflake-orange)](https://duckdb.org)
[![Data Validation](https://img.shields.io/badge/validation-Pydantic%20v2-red)](https://docs.pydantic.dev)

A production-grade, modular ETL (Extract, Transform, Load) pipeline built with Python 3.12. This project orchestrates the flow of financial data from the National Bank of Poland (NBP), performing multi-stage validation, stateful anomaly detection, and automated visual reporting.

---

## 🚀 Key Features

*   **Multi-Source Ingestion:** Concurrent handling of foreign exchange rates and precious metals (Gold) data.
*   **Stateful Data Quality (Guardrails):** Implements a "Volatility Check" that compares incoming data against historical database records to flag potential API errors or market anomalies.
*   **Advanced Analytics & Reporting:** Automated generation of Matplotlib charts, including individual currency trend lines and dual-axis correlation analysis (e.g., Gold Price vs. USD).
*   **Professional Storage:** High-performance DuckDB integration with an *Idempotent Load* strategy (using SQL `NOT EXISTS` logic) to ensure zero data duplication.
*   **Hybrid Architecture:** Scalable design supporting both local fast analytics (DuckDB) and enterprise data warehousing (Azure Blob Storage + Snowflake).

---

## 🛠 Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Language** | Python 3.12 |
| **Data Validation** | Pydantic v2 |
| **Data Manipulation** | Pandas |
| **Local OLAP Database** | DuckDB (In-process) |
| **Cloud Data Warehouse** | Snowflake |
| **Cloud Storage (Landing)** | Azure Blob Storage |
| **Visualization** | Matplotlib |
| **Environment & Paths** | Pathlib, Python-dotenv |

---

## 📂 Project Structure

```text
Automated_Data_Pipeline/
├── data/
│   ├── database/          # DuckDB storage (.duckdb)
│   ├── raw/               # Archived raw JSON responses
│   └── reports/           # Automated PNG charts & analytics
├── src/
│   ├── analytics/         # CLI parser & Reporting engine
│   ├── ingestion/         # API connectors (NBP, Gold)
│   ├── models/            # Pydantic schemas (Data Contracts)
│   ├── processing/        # Validation, Transformation & Quality Checks
│   └── storage/           # Database managers (DuckDB)
├── .gitignore             # Git exclusion rules
├── main.py                # Orchestrator (The "Brain")
└── requirements.txt       # Dependency list
```

## ⚙️ Getting Started

### 1. Installation & Setup

Clone the repository and set up the virtual environment:

```bash
# Clone the repository
git clone [https://github.com/your-username/automated_data_pipeline.git](https://github.com/your-username/automated_data_pipeline.git)
cd automated_data_pipeline

# Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Running the Pipeline
# The application features a powerful CLI. You can customize the run without touching the code:

# Basic run for USD and EUR
python main.py --currencies USD,EUR

# Advanced run: 30 days of history, gold prices enabled, and 5% anomaly threshold
python main.py --currencies USD,GBP,CHF --days 30 --check-gold --threshold 0.05
```

📊 Data Insights & Quality
The pipeline doesn't just move data; it ensures it's correct.
- Validation: Every API response is checked against a Pydantic model. If the schema changes, the pipeline fails safely.
- Anomaly Detection: If a currency moves more than X% (default 10%) compared to the last database entry, it is flagged in the is_anomaly column and a warning is logged.
- Visual Analytics: The system automatically generates a correlation chart between Gold and USD, allowing for quick visual market analysis.

🏗 Architecture
Extraction: Python script fetches JSON data from NBP API.
Landing Zone: Data is uploaded to Azure Blob Storage (Bronze Layer).
Data Warehouse: Snowflake ingests raw JSON via Storage Integration.
Transformation: SQL Views transform semi-structured JSON into relational tables (Silver Layer).

❄️ Snowflake Setup
The SQL scripts in /snowflake directory follow the Medallion Architecture:

- 01_setup: RBAC and Databases.
- 02_integration: Cloud connectivity.
- 03_bronze: Raw data ingestion.
- 04_silver: Data cleaning and typing.
- 05_gold: Data analysis

📈 Future Roadmap
- CI/CD Integration: Automated testing and linting via GitHub Actions.
- Containerization: Full Docker support for cloud deployment.
- Alerting: Integration with Telegram/Slack API for real-time anomaly notifications.
- Orchestration: Migration to Apache Airflow for complex scheduling.
