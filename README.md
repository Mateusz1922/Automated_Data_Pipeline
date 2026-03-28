📈 Professional Market Data ETL & Analytics Pipeline
A production-grade, modular ETL (Extract, Transform, Load) pipeline built with Python 3.12. This project orchestrates the flow of financial data from the National Bank of Poland (NBP), performing multi-stage validation, stateful anomaly detection, and automated visual reporting.

🚀 Key Features
Multi-Source Ingestion: Concurrent handling of foreign exchange rates and precious metals (Gold) data.

Stateful Data Quality (Guardrails): Implements a "Volatility Check" that compares incoming data against historical database records to flag potential API errors or market anomalies.

Advanced Analytics & Reporting: Automated generation of Matplotlib charts, including:

Individual currency trend lines.

Dual-axis correlation analysis (e.g., Gold Price vs. USD Exchange Rate).

Robust CLI Interface: Fully configurable via command-line arguments (currencies, history depth, anomaly thresholds).

Professional Storage: High-performance DuckDB integration with an Idempotent Load strategy (using SQL NOT EXISTS logic) to ensure zero data duplication even on repeated runs.

Clean Architecture: Strict separation of concerns following SOLID principles.

🛠 Tech Stack
Language: Python 3.12

Data Validation: Pydantic v2

Data Manipulation: Pandas

Database: DuckDB (In-process OLAP)

Visualization: Matplotlib

Environment: Pathlib (OS-agnostic paths), Dotenv

📂 Project Structure
Automated_Data_Pipeline/
├── data/
│   ├── raw/               # Archived raw JSON responses
│   ├── database/          # DuckDB storage (.duckdb)
│   └── reports/           # Automated PNG charts & analytics
├── src/
│   ├── ingestion/         # API connectors (NBP, Gold)
│   ├── models/            # Pydantic schemas (Data Contracts)
│   ├── processing/        # Validation, Transformation & Quality Checks
│   ├── storage/           # Database managers (DuckDB)
│   └── analytics/         # CLI parser & Reporting engine
├── main.py                # Orchestrator (The "Brain")
├── requirements.txt       # Dependency list
└── .gitignore             # Git exclusion rules

⚙️ Usage
Installation

1. Clone & Setup:

### Bash
git clone https://github.com/your-username/automated_data_pipeline.git
cd automated_data_pipeline
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

Running the Pipeline
The application features a powerful CLI. You can customize the run without touching the code:

### Bash
-- Basic run for USD and EUR
python main.py --currencies USD,EUR

-- Advanced run: 30 days of history, gold prices enabled, and 5% anomaly threshold
python main.py --currencies USD,GBP,CHF --days 30 --check-gold --threshold 0.05

📊 Data Insights & Quality
The pipeline doesn't just move data; it ensures it's correct.

Validation: Every API response is checked against a Pydantic model. If the schema changes, the pipeline fails safely.

Anomaly Detection: If a currency moves more than X% (default 10%) compared to the last database entry, it is flagged in the is_anomaly column and a warning is logged.

Visual Analytics: The system automatically generates a correlation chart between Gold and USD, allowing for quick visual market analysis.

📈 Future Roadmap
CI/CD Integration: Automated testing and linting via GitHub Actions.

Containerization: Full Docker support for cloud deployment.

Alerting: Integration with Telegram/Slack API for real-time anomaly notifications.

Orchestration: Migration to Apache Airflow for complex scheduling.