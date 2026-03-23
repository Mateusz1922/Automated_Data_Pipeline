Automated NBP Currency Data Pipeline
A robust, modular ETL (Extract, Transform, Load) pipeline built with Python 3.12. This project fetches currency exchange rates from the National Bank of Poland (NBP) API, validates the data structure, transforms it into an analytical format, and stores it in a high-performance DuckDB database.

🚀 Key Features
Automated Ingestion: Periodically fetches raw JSON data from the NBP API.

Data Validation: Uses Pydantic v2 for strict type checking and schema validation ("Fail-fast" approach).

Transformation & Enrichment: Leverages Pandas to clean data, convert types, and add audit metadata (timestamps).

Efficient Storage: Implements an Idempotent Load (Upsert logic) into DuckDB to prevent data duplication.

Modular Architecture: Separation of concerns (Ingestion, Processing, Transformation, Storage) for easy testing and scalability.

🛠 Tech Stack
Language: Python 3.12

Data Validation: Pydantic

Data Manipulation: Pandas

Database: DuckDB (OLAP-optimized)

Networking: Requests

Environment Management: Dotenv & Virtualenv

📂 Project Structure

automated_data_pipeline/
├── data/
│   ├── raw/               # Archived raw JSON responses from API
│   └── database/          # DuckDB database files (.duckdb)
├── src/
│   ├── ingestion.py       # API communication and raw storage
│   ├── models.py          # Pydantic schemas (Data Quality)
│   ├── processing.py      # File management and validation logic
│   ├── transformation.py  # Pandas-based data cleaning/enrichment
│   └── database.py        # DuckDB connection and SQL execution
├── main.py                # Entry point (Orchestrator)
├── requirements.txt       # Dependency list
└── .env                   # Configuration & API keys (hidden)

📊 Data Pipeline Workflow
Extract: The DataIngestor class fetches a JSON response from the NBP API and saves it to a timestamped file in data/raw/.

Validate: DataProcessor finds the latest file and maps the raw JSON to a Pydantic RateTable model, ensuring all fields meet expectations.

Transform: DataTransformer converts the validated object into a Pandas DataFrame, cleans column types, and calculates inverted rates.

Load: DatabaseManager handles the SQL connection to DuckDB, ensuring that records are only inserted if they don't already exist (deduplication based on code and effective_date).

📈 Future Improvements
CI/CD: Add GitHub Actions to run automated tests on every push.

Containerization: Wrap the application in a Docker container.

Orchestration: Integrate Apache Airflow or Prefect for advanced scheduling and monitoring.

Cloud Integration: Export processed data to AWS S3 or Azure Blob Storage.